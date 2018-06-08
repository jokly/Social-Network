from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class OAuthLoginForm(FlaskForm):
    login = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class OAuthGetAccessForm(FlaskForm):
    get_access = SubmitField('OK')

class AcceptOAuth(FlaskForm):
    submit = SubmitField('OK')
