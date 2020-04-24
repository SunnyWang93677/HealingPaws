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

class cus_SignupForm(FlaskForm):

    cus_username = StringField('Username', validators=[DataRequired()])
    cus_real_name = StringField('Real name', validators=[DataRequired()])
    email = StringField('e-mail', validators=[DataRequired()])
    phone = StringField('phone number', validators=[DataRequired()])
    cus_password_hash= PasswordField('Password', validators=[DataRequired()])
    cus_password_hash2= PasswordField('Repeat Password', validators=[DataRequired()])

    submit = SubmitField('sign up')


class AnswerForm(FlaskForm):
    answer = TextAreaField('Answer Field')
    save = SubmitField('Save')


class QuestionForm(FlaskForm):
    question = TextAreaField('Question Field')
    save = SubmitField('Save')