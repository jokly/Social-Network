import os
from flask import render_template, flash, redirect, url_for, request, send_from_directory
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from datetime import datetime
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from app.models import User

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

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
            avatar = request.files['avatar']
            file_name = '{}.jpg'.format(user.id)
            img_path = os.path.join(app.config['AVATARS_FOLDER'], file_name)
            avatar.save(img_path)

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

@app.route('/edit_profile')
@login_required
def edit_profile():
    form = EditProfileForm()

    if form.validate_on_submit():
        pass

    return render_template('edit_profile.html', title='Edit profile', form=form)
