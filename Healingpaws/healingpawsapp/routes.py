from flask import render_template, flash, redirect, url_for, session, send_file, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from healingpawsapp import app, db
from healingpawsapp.forms import LoginForm
# from appdir.models import User, Post, Profile
from healingpawsapp.config import Config
from healingpawsapp.models import Customer,Employee
import os
import re

app.config['UPLOAD_PHOTO'] = Config.PHOTO_UPLOAD_DIR



@app.route('/')
@app.route('/home')
def home():
    return render_template('main.html')


@app.route('/employee')
def employee():
    return render_template('employee.html')


@app.route('/emp_homepage')
def emp_homepage():
    return 'hello word'


@app.route('/employee_login', methods=['GET', 'POST'])
def employee_login():
    form = LoginForm()
    if form.validate_on_submit():
        employee_in_db = Employee.query.filter(Employee.emp_username == form.username.data).first()
        if not employee_in_db:
            flash('No user found with username: {}'.format(form.username.data))
            return redirect(url_for('employee_login'))
        #check_password_hash(user_in_db.password_hash, form.password.data):
        if check_password_hash(employee_in_db.emp_password_hash,form.password.data):
            flash('Login success!')
            session["EMPID"] = employee_in_db.emp_id
            if form.remember_me:
                session.permanent = True
            flash("login success, your user name is :"+str(form.username))
            return redirect('/emp_homepage')
        else:
            flash('your password is incorrect')
            return redirect(url_for('employee_login'))
    return render_template('employee_login.html', title='Employee Login', form=form)


@app.route('/emp_register', methods=['GET', 'POST'])
def emp_register():
    if request.method == 'GET':
        return render_template('employee_register.html', title='emp_register')
    else:
        print(request.form)
        emp_username = request.form.get('emp_username')
        emp_real_name = request.form.get('emp_real_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        customer = Employee.query.filter(Employee.emp_username == emp_username).first()
        if customer:
            flash('This username has been registered,please login')
            return redirect(url_for('emp_register'))
        else:
            if password != password2:
                print('not match')
                flash('password has not match')
                return redirect(url_for('emp_register'))
            else:
                passw_hash = generate_password_hash(password)
                employee = Employee(emp_username=emp_username, emp_password_hash=passw_hash, emp_real_name=emp_real_name,
                                    email=email, phone=phone)
                db.session.add(employee)
                db.session.commit()
                flash("register success")
                return redirect(url_for('employee_login'))


@app.route('/index')
def index():
    return render_template('index.html', title='index')



@app.route('/customer_login', methods=['GET', 'POST'])
def customer_login():
    if request.method == 'GET':
        return render_template('customer_login.html', title='customer_login')
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



@app.route('/cus_register', methods=['GET', 'POST'])
def cus_register():
    if request.method == 'GET':
        return render_template('cus_register.html', title='cus_register')
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
                customer = Customer(cus_username=cus_username, cus_password_hash=cus_password,
                                    cus_real_name=cus_real_name,
                                    email=email, phone=phone)
                db.session.add(customer)
                db.session.commit()
                return redirect(url_for('index'))


def show_error(judge=False):
    if judge:
        return not session.get("EMPID")
    return redirect('/emp_login')


@app.route('/cus_mainpage',methods=['GET','POST'])
def cus_mainpage():
    if show_error(True):
        return show_error()
    if request.method == 'GET':
        return render_template('customer-mainpage.html', title='cus_register')


@app.route('/cus_appointment',methods=['GET','POST'])
def cus_appointment():
    return 'lalala'
