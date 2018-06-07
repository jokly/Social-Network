import os
from datetime import datetime
from sqlalchemy import text
from flask import render_template, flash, redirect, url_for, request, send_from_directory
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from app import app, db
from app.forms.AddPostForm import AddPostForm
from app.forms.EditProfileForm import EditProfileForm
from app.forms.LoginForm import LoginForm
from app.forms.RegistrationForm import RegistrationForm
from app.models import User, Post
from app.models import user_avatar_url, user_info, post_img_url

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

def save_file(file_name, file_folder, file_data):
    file_name = '{}.jpg'.format(file_name)
    img_path = os.path.join(app.config[file_folder], file_name)
    file_data.save(img_path)

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
    posts = []
    for root in root_posts:
        query = text('SELECT get_comments({}); FETCH ALL IN _result;'.format(root.id))
        result = db.engine.execute(query)
        comments = []
        for row in result:
            comments.append(row)
        
        comments = comments[1:len(comments)]
        posts.append(dict(root=root, comments=comments))

    return render_template('index.html', title='Home', add_post_form=add_post_form, posts=posts,
        user_avatar_url=user_avatar_url, user_info=user_info, post_img_url=post_img_url)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

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

    return render_template('login.html', title='Log In', form=form)

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
    page_title = user.name + ' ' + user.surname

    return render_template('user.html', title=page_title, user=user)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()

    if form.validate_on_submit():
        User.query.filter_by(id=current_user.id).update(dict(email=form.email.data,
            name=form.name.data, surname=form.surname.data, age=form.age.data, city=form.city.data))
        
        db.session.commit()

        return redirect(url_for('user', login=current_user.login))

    return render_template('edit_profile.html', title='Edit profile', form=form, user=current_user)
