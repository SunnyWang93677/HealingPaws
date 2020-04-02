from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, RadioField, DateField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
	username = StringField('username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password', validators=[DataRequired()])
	submit = SubmitField('Sign In')