from flask import render_template, flash, redirect, url_for, session, send_file, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from healingpawsapp import app, db
from healingpawsapp.forms import LoginForm
#from appdir.models import User, Post, Profile
from healingpawsapp.config import Config
from healingpawsapp.models import Customer,Employee
import os
import re


app.config['UPLOAD_PHOTO'] = Config.PHOTO_UPLOAD_DIR


@app.route('/')
@app.route('/home')
def home():
    return 'hello word'

@app.route('/index')
def index():
    return render_template('index.html',title='index')

@app.route('/customer_login/',methods=['GET','POST'])
def customer_login():
    if request.method == 'GET':
        return render_template('customer_login.html',title='customer_login')
    else:
        phone = request.form.get('phone')
        password = request.form.get('password')
        customer = Customer.query.filter(Customer.email == phone, Customer.password_hash == password).first()
        if customer:
            session['cus_id'] = Customer.cus_id
            session.permanent = True
            return redirect(url_for('home'))
        else:
            return 'phone does not exist or password is wrong!'

@app.route('/employee_login/',methods=['GET','POST'])
def customer_login():
    if request.method == 'GET':
        return render_template('employee_login.html',title='employee_login')
    else:
        email = request.form.get('email')
        password = request.form.get('password')
        employee = Employee.query.filter(Employee.email == email, Employee.password_hash == password).first()
        if employee:
            session['emp_id'] = Employee.emp_id
            session.permanent = True
            return redirect(url_for('home'))
        else:
            return 'email does not exist or password is wrong!'

@app.route('/cus_register/',methods=['GET','POST'])
def cus_register():
    if request.method == 'GET':
        return render_template('cus_register.html',title='cus_register')
    else:
        cus_username = request.form.get('cus_username')
        cus_real_name = request.form.get('cus_real_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        cus_password = request.form.get('cus_password_hash')
        cus_password_2 = request.form.get('cus_password_hash2')
        customer = Customer.query.filter(Customer.cus_username == cus_username).first()
        if customer:
            return 'This username has been registered'
        else:
            if cus_password != cus_password_2:
                return 'password has not match'
            else:
                customer = Customer(cus_username=cus_username, cus_password_hash=cus_password, cus_real_name = cus_real_name,
                                    email = email, phone = phone  )
                db.session.add(customer)
                db.session.commit()
                return redirect(url_for('index'))

@app.route('/emp_register/',methods=['GET','POST'])
def emp_register():
    if request.method == 'GET':
        return render_template('emp_register.html',title='emp_register')
    else:
        emp_username = request.form.get('emp_username')
        emp_real_name = request.form.get('emp_real_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        title = request.form.get('title')
        employee = Employee.query.filter(Employee.emp_username == emp_username).first()
        if employee:
            return 'This username has been registered'
        else:
            if password != password2:
                return 'password has not match'
            else:
                employee = Employee(emp_username=emp_username, emp_password_hash =password, emp_real_name = emp_real_name,
                                    email = email, phone = phone ,title = title )
                db.session.add(employee)
                db.session.commit()
                return redirect(url_for('index'))