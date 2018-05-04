from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask import url_for
from app import db, login

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120))
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(64))
    surname = db.Column(db.String(64))
    age = db.Column(db.Integer)
    sex = db.Column(db.String(32))
    city = db.Column(db.String(64))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def user_url(self):
        return url_for('user', login=self.login)

    def __repr__(self):
        return '<User {}>'.format(self.login) 

@login.user_loader
def loader_user(id):
    return User.query.get(int(id))
