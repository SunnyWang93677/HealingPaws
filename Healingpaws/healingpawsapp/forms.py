from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, RadioField, FileField, \
    TextAreaField
from wtforms.validators import DataRequired, ValidationError
from flask_wtf.file import FileRequired, FileAllowed


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class AnswerForm(FlaskForm):
    answer = TextAreaField('Answer Field')
    save = SubmitField('Save')


class QuestionForm(FlaskForm):
	question = TextAreaField('Question Field')
	save = SubmitField('Save')
