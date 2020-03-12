from flask import render_template, flash, redirect, url_for, session, send_file, request, jsonify
#from werkzeug.security import generate_password_hash, check_password_hash
from Healingpaws.healingpawsapp import app, db
#from Healingpaws.healingpawsapp.forms import LoginForm, SignupForm, ProfileForm, PostForm, AddPhotoForm
#from Healingpaws.healingpawsapp.models import User, Post, Profile
from Healingpaws.healingpawsapp.config import Config
import os
import re

app.config['UPLOAD_PHOTO'] = Config.PHOTO_UPLOAD_DIR


@app.route('/')
@app.route('/home')
def home():
    #user = {'username': 'Agnes'}
    #return render_template('home.html', user=user)
    return "Hello word"
