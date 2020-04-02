from flask import render_template, flash, redirect, url_for, session, send_file, request, jsonify
#from werkzeug.security import generate_password_hash, check_password_hash
from healingpawsapp import app, db
#from healingpawsapp.forms import LoginForm, SignupForm, ProfileForm, PostForm, AddPhotoForm
#from appdir.models import User, Post, Profile
from healingpawsapp.config import Config
import os
import re

from healingpawsapp.formes import QuestionForm
from healingpawsapp.models import Customer

app.config['UPLOAD_PHOTO'] = Config.PHOTO_UPLOAD_DIR


@app.route('/')
@app.route('/home')
def home():
    return 'hello word'
@app.route('/question',methods=['GET', 'POST'])
def question():
    form = QuestionForm()
    if not session.get('USERNAME') is None:
        user_in_db = Customer.query.filter(Customer.cus_username == session.get("USERNAME")).first()
        username = user_in_db.username
        if form.validate_on_submit():
            return render_template('question.html', username=username, title=username,question = form)
        else:
