from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, SelectField, IntegerField, BooleanField, FileField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import User

class LoginForm(FlaskForm):
    login = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    login = StringField('Login', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    name = StringField('Name', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    sex = SelectField('Sex', validators=[DataRequired()], choices=[('male', 'Male'), ('female', 'Female')])
    city = StringField('City', validators=[DataRequired()])
    avatar = FileField('Avatar file', validators=[FileAllowed(['jpg'], 'Images only')])
    submit = SubmitField('Register')

    def validate_login(self, login):
        user = User.query.filter_by(login=login.data).first()
        if user is not None:
            raise ValidationError('Please use a different login')

    def validate_age(self, age):
        age = int(age.data)

        if age <= 0 or age > 100:
            raise ValidationError('Invalid age')

class EditProfileForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    name = StringField('Name', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    sex = SelectField('Sex', validators=[DataRequired()], choices=[('male', 'Male'), ('female', 'Female')])
    city = StringField('City', validators=[DataRequired()])
    avatar = FileField('Avatar file', validators=[FileAllowed(['jpg'], 'Images only')])
    submit = SubmitField('Submit')
