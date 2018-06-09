import os
import urllib
from datetime import datetime
import requests
import uuid
from sqlalchemy import text
from flask import render_template, flash, redirect, url_for, request, send_from_directory, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from app import app, db
from app.forms.AddPostForm import AddPostForm
from app.forms.EditProfileForm import EditProfileForm
from app.forms.LoginForm import LoginForm
from app.forms.OAuthLoginForm import OAuthLoginForm, OAuthGetAccessForm, AcceptOAuth
from app.forms.RegistrationForm import RegistrationForm
from app.models import User, Post
from app.models import ExternalSocialNetwork, ExternalSocialNetworkSession, AuthorizationCode, AccessToken
from app.models import user_avatar_url, user_info, post_img_url

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

def save_file(file_name, file_folder, file_data):
    file_name = '{}.jpg'.format(file_name)
    
    if not os.path.exists(app.config[file_folder]):
        os.makedirs(app.config[file_folder])

    img_path = os.path.join(app.config[file_folder], file_name)
    file_data.save(img_path)

def get_posts(root_posts):
    posts = []
    for root in root_posts:
        query = text('SELECT get_comments({}); FETCH ALL IN _result;'.format(root.id))
        result = db.engine.execute(query)
        comments = []
        for row in result:
            comments.append(row)
        
        comments = comments[1:len(comments)]
        posts.append(dict(root=root, comments=comments))

    return posts

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    add_post_form = AddPostForm()

    if add_post_form.validate_on_submit():
        parent_post_id = None if add_post_form.post_id.data == 'None' else add_post_form.post_id.data
        post = Post(text=add_post_form.text.data, author=current_user.id, parent_post=parent_post_id)
        db.session.add(post)
        db.session.commit()

        if add_post_form.img.data:
            save_file(post.id, 'POSTS_IMG_FOLDER', request.files['img'])

        return redirect(url_for('index'))

    root_posts = Post.query.filter(Post.parent_post.is_(None)).order_by(Post.timestamp.desc())
    posts = get_posts(root_posts)

    return render_template('index.html', title='Home', add_post_form=add_post_form, posts=posts,
        user_avatar_url=user_avatar_url, user_info=user_info, post_img_url=post_img_url)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    socials = ExternalSocialNetwork.query.all()

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(login=form.login.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('Invalid login or password')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)

        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')

        return redirect(next_page)

    return render_template('login.html', title='Log In', socials=socials, form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(login=form.login.data, email=form.email.data, 
            name=form.name.data, surname=form.surname.data, age=form.age.data,
            sex=form.sex.data, city=form.city.data)

        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        if form.avatar.data:
            save_file(user.id, 'AVATARS_FOLDER', request.files['avatar'])

        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    elif form.errors:
        flash('Input field errors')

    return render_template('register.html', title='Register', form=form)

@app.route('/uploads/<path:file_path>')
def uploaded_file(file_path):
    return send_from_directory(app.config['STATIC_FOLDER'], file_path)

@app.route('/user/<login>')
@login_required
def user(login):
    user = User.query.filter_by(login=login).first_or_404()
    page_title = str(user.name) + ' ' + str(user.surname)

    root_posts = Post.query.filter(Post.author == current_user.id).order_by(Post.timestamp.desc())
    posts = get_posts(root_posts)

    return render_template('user.html', title=page_title, user=user, posts=posts,
        user_avatar_url=user_avatar_url, user_info=user_info, post_img_url=post_img_url)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()

    if form.validate_on_submit():
        User.query.filter_by(id=current_user.id).update(dict(login=form.login.data, email=form.email.data,
            name=form.name.data, surname=form.surname.data, age=form.age.data, city=form.city.data))
        
        db.session.commit()

        return redirect(url_for('user', login=current_user.login))

    return render_template('edit_profile.html', title='Edit profile', form=form, user=current_user)

def get_auth_code(service_id):
    auth_code = AuthorizationCode(service_id=service_id, user_id=current_user.id)
    db.session.add(auth_code)
    db.session.commit()

    return auth_code.code

@app.route('/api/login', methods=['GET', 'POST'])
def api_login():
    form = None

    if current_user.is_authenticated:
        form = OAuthGetAccessForm()
    else:
        form = OAuthLoginForm()

    next_page = request.args.get('redirect_url')
    service_id = request.args.get('service_id')
    if next_page is None or service_id is None:
        next_page = None

    if form.validate_on_submit():
        if current_user.is_authenticated:
            return redirect('{}?auth_code={}'.format(next_page, get_auth_code(service_id)))

        user = User.query.filter_by(login=form.login.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('Invalid login or password')
            return redirect('{}?redirect_url={}'.format(url_for('api_login'), next_page))

        login_user(user)

        return redirect('{}?auth_code={}'.format(next_page, get_auth_code(service_id)))

    return render_template('oauth_login.html', title='SocialNetwork', form=form, next_page=next_page)

@app.route('/api/token', methods=['GET', 'POST'])
def get_token():
    code = request.form.get('auth_code')
    service_id = request.form.get('service_id')

    if code is None or service_id is None:
        return jsonify(status='error')

    auth_code = AuthorizationCode.query.filter_by(service_id=service_id, code=code).first()

    if auth_code is None:
        return jsonify(status='error')

    access_token = AccessToken(user_id=auth_code.user_id, service_id=service_id)
    db.session.add(access_token)
    db.session.delete(auth_code)
    db.session.commit()

    return jsonify(status='ok', user_id=access_token.user_id, token=access_token.token)

@app.route('/api/profile/<user_id>', methods=['GET', 'POST'])
def get_profile_info(user_id):
    service_id = request.args.get('service_id')
    token = request.args.get('token')

    if user_id is None or token is None or service_id is None:
        return jsonify(status='error')

    access_token = AccessToken.query.filter_by(service_id=service_id, user_id=user_id, token=token).first()

    if access_token is None:
        return jsonify(status='error')

    user = User.query.filter_by(id=user_id).first()

    return jsonify(status='ok', login=user.login, email=user.email)

@app.route('/api/posts/<user_id>', methods=['GET', 'POSTS'])
def api_get_posts(user_id):
    service_id = request.args.get('service_id')

    if service_id is None:
        return jsonify(status='error')

@app.route('/accept_social_login/<sn_name>', methods=['GET', 'POST'])
def accept_social_login(sn_name):
    auth_code = request.args.get('auth_code')

    if auth_code is None:
        return render_template('accept_social_login.html', bad_response=True)

    form = AcceptOAuth()

    if form.is_submitted():
        service = ExternalSocialNetwork.query.filter_by(name=sn_name).first()

        if service is None:
            return render_template('accept_social_login.html', bad_response=True)

        token = requests.post('{}/api/token'.format(service.url),
            data={'service_id': 'vl-social', 'auth_code': auth_code}).json()
        
        if token['status'] == 'error':
            return render_template('accept_social_login.html', bad_response=True)

        external_token = ExternalSocialNetworkSession.query.filter_by(ext_uid=token['user_id'], ext_social_network=service.id).first()

        if external_token is None:
            new_user = User(login=uuid.uuid4())
            new_user.set_password(str(uuid.uuid4()))
            db.session.add(new_user)
            db.session.commit()

            login_user(new_user)

            external_sn = ExternalSocialNetworkSession(user=current_user.id, access_token=token['token'],
                ext_uid=token['user_id'], ext_social_network=service.id)
            db.session.add(external_sn)
            db.session.commit()
        else:
            user = User.query.filter_by(id=external_token.user).first()
            login_user(user)

        return redirect(url_for('index'))

    return render_template('accept_social_login.html', title='Accept Login', form=form, sn_name=sn_name)
