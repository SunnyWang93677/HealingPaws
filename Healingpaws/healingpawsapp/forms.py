from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField,DateField, RadioField, FileField, \
    TextAreaField
from wtforms.validators import DataRequired, ValidationError,Regexp,EqualTo
from flask_wtf.file import FileRequired, FileAllowed


class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Sign In')

class cus_SignupForm(FlaskForm):
	username = StringField('username', validators=[Regexp(r".{2,20}", message='Incorrect format')])
	realname = StringField('realname', validators=[Regexp(r".{2,20}", message='Incorrect format')])
	phonenumber = StringField('phonenumber', validators=[Regexp(r"1[345678]\d{9}",message='wrong phone number')])
	password = PasswordField('password1', validators=[Regexp(r"[0-9a-zA-Z_\.]{6,20}",message='Incorrect format')])
	password2 = PasswordField('password2', validators=[EqualTo("password1" ,message='The two passwords not same')])
	# accept_rules = BooleanField('I accept the site rules', validators=[DataRequired()])
	email = StringField('email', validators=[Regexp(r"^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$", message='wrong email format')])
	submit = SubmitField('register')

class AppointmentForm(FlaskForm):
	petid = StringField('Petid', validators=[DataRequired()])
	cus_id = StringField('Cusid', validators=[DataRequired()])
	type = SelectField('type', validators=[DataRequired()])
	Place = SelectField('Place', validators=[DataRequired()])
	date = DateField('Date', validators=[DataRequired()])
	Comment = TextAreaField("Comment", validators=[DataRequired()])
	submit = SubmitField('Submit')

class PetForm(FlaskForm):
	name = StringField('name', validators=[DataRequired()])
	gender = SelectField('gender', validators=[DataRequired()])
	type = StringField('type', validators=[DataRequired()])
	birthday = DateField('birthday', validators=[DataRequired()])
	submit = SubmitField('Submit')

class QuestionForm(FlaskForm):
	body = StringField('Body', validators=[DataRequired()])
	submit = SubmitField('Post')

class AnswerForm(FlaskForm):
	body = StringField('Body', validators=[DataRequired()])
	questionid = StringField('Questionid', validators=[DataRequired()])
	submit = SubmitField('answer')
