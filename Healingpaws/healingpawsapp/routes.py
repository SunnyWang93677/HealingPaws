from flask import render_template, flash, redirect, url_for, session, send_file, request, jsonify
#from werkzeug.security import generate_password_hash, check_password_hash
from healingpawsapp import app, db
#from healingpawsapp.forms import LoginForm, SignupForm, ProfileForm, PostForm, AddPhotoForm
#from appdir.models import User, Post, Profile
from healingpawsapp.config import Config
import os
import re

app.config['UPLOAD_PHOTO'] = Config.PHOTO_UPLOAD_DIR


@app.route('/')
@app.route('/home')
def home():
    return 'hello word'