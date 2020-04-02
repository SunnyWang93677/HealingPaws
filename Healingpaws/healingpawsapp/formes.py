from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, RadioField, FileField, \
    TextAreaField
from wtforms.validators import DataRequired, ValidationError
from flask_wtf.file import FileRequired, FileAllowed
class AnswerForm(FlaskForm):
    answer = TextAreaField('Answer Field')
    save = SubmitField('Save')

class QuestionForm(FlaskForm):
    question = TextAreaField('Question Field')
    save = SubmitField('Save')