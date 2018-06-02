from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import FileField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class AddPostForm(FlaskForm):
    text = TextAreaField('Text', validators=[DataRequired(), Length(3, 500, 'Invalid post length')])
    img = FileField('Attach image', validators=[FileAllowed(['jpg'], 'Images only')])
    submit = SubmitField('Submit')
