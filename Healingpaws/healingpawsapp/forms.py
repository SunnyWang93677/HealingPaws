from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, RadioField, DateField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
	username = StringField('username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Password2', validators=[DataRequired()])
	submit = SubmitField('Sign In')