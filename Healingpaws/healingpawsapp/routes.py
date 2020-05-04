from flask import render_template, flash, redirect, url_for, session, send_file, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from healingpawsapp import app, db
# from appdir.models import User, Post, Profile
from healingpawsapp.config import Config
from healingpawsapp.models import Customer, Employee, Question, Answer
import os
import re

app.config['UPLOAD_PHOTO'] = Config.PHOTO_UPLOAD_DIR


@app.route('/')
@app.route('/home',methods=['GET', 'POST'])
def home():
    return render_template('base.html')


@app.route('/employee_login', methods=['GET', 'POST'])
def employee_login():
    if request.method == 'GET':
        return render_template('employee_login.html', title='employee_login')
    else:
        email = request.form.get('email')
        password = request.form.get('password')
        print(email,password)
        employee = Employee.query.filter(Employee.email == email).first()
        if employee:
            if check_password_hash(employee.emp_password_hash, password):
                session['EMPID'] = employee.emp_id
                if request.form.get('remember') == 1:
                    session.permanent = True
                else:
                    session.permanent = False
                return redirect(url_for('employee_main'))
            else:
                flash('Your password is incorrect, please try again')
                return redirect(url_for('employee_login'))
        else:
            flash('the user is not exist, please register first')
            return redirect(url_for('employee_login'))

@app.route('/version')
def version():
    return '123'

@app.route('/employee_register', methods=['GET', 'POST'])
def employee_register():
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
        customer = Employee.query.filter(Employee.email == email).first()
        if customer:
            flash('This username has been registered,please login')
            return redirect(url_for('employee_register'))
        else:
            if password != password2:
                print('not match')
                flash('password has not match')
                return redirect(url_for('employee_register'))
            else:
                passw_hash = generate_password_hash(password)
                employee = Employee(emp_username=emp_username, emp_password_hash=passw_hash, emp_real_name=emp_real_name,
                                    email=email, phone=phone)
                db.session.add(employee)
                db.session.commit()
                flash("register success")
                return redirect(url_for('employee_login'))



@app.route('/employee', methods=['GET', 'POST'])
def employee():
    return render_template('employee.html')


@app.route('/employee_main', methods=['GET', 'POST'])
def employee_main():
    return render_template('employee_main.html')



@app.route('/employee_question', methods=['GET','POST'])
def employee_qa():
    if request.method == 'GET':
        if session['EMPID']:
            questions = Question.query.all()
            return render_template('employee_q&a.html',questions=questions)
        if session['CUSID']:
            flash('Limit Enter')
            return redirect(url_for('cus_mainpage'))
    else:
        return ''

@app.route('/employee_appointment', methods=['GET','POST'])
def employee_ap():
    return render_template('employee_appointment')


@app.route('/index')
def index():
    return render_template('index.html', title='index')


@app.route('/customer_login', methods=['GET', 'POST'])
def customer_login():
    if request.method == 'GET':
        return render_template('customer-login.html', title='customer_login')
    else:
        email = request.form.get('email')
        password = request.form.get('password')
        print(email,'++',password)
        if (email is not None) and (password is not None):
            customer = Customer.query.filter(Customer.email == email).first()
            if customer:
                if check_password_hash(customer.cus_password_hash, password):
                    session['CUSID'] = customer.cus_id
                    if request.form.get('remember') == 1:
                        session.permanent = True
                    else:
                        session.permanent = False
                    return redirect(url_for('customer_mainpage'))
                else:
                    flash('Your password is incorrect, please try again')
                    return redirect(url_for('customer_login'))
            else:
                flash('the user is not exist, please register first')
                return redirect(url_for('customer_login'))
        else:
            return ''

@app.route('/ttt',methods=['GET','POST'])
def tanchuang():
    if request.method=='POST':
        print(request.form.get('aa'))
        if(request.form.get('aa')=='123456'):
            return 'password correct'
        else:
            return 'the password is wrong'
    return render_template('tanchuangchuang.html')

@app.route('/customer_register', methods=['GET', 'POST'])
def customer_register():
    if request.method == 'GET':
        return render_template('customer-register.html', title='cus_register')
    else:
        cus_username = request.form.get('username')
        cus_real_name = request.form.get('realname')
        email = request.form.get('email')
        phone = request.form.get('phonenumber')
        cus_password = request.form.get('password1')
        cus_password_2 = request.form.get('password2')
        customer_db = Customer.query.filter(Customer.email == email).first()
        if customer_db:
            print('This username has been registered')
            return redirect(url_for('customer_register'))
        else:
            if cus_password != cus_password_2:
                print('password has not match')
                return redirect(url_for('customer_register'))
            else:
                cus_password_hash = generate_password_hash(cus_password)
                customer = Customer(cus_username=cus_username, cus_password_hash=cus_password_hash,
                                    cus_real_name=cus_real_name,
                                    email=email, phone=phone)
                print(customer)
                db.session.add(customer)
                db.session.commit()
                return redirect(url_for('customer_login'))

@app.route('/customer_question',methods=['GET','POST'])
def customer_question():
    if request.method == 'GET':
        if session.get('CUSID'):
            data = Question.query.filter(Question.cus_id == session.get('CUSID'))
            return render_template('customer-question.html', title='Question', questionlist=data)

        else:
            return redirect(url_for('customer_login'))
    else:
        if session.get('CUSID'):
            title = request.form.get('title')
            question = request.form.get('comment')



@app.route('/customer_question/<qus_id>',methods=['GET','POST'])
def detail(qus_id):
    if request.method == 'GET':
        if session.get('CUSID'):
            question = Question.query.filter(Question.cus_id == qus_id).first()
            answer = Answer.query.filter(Answer.que_id == qus_id)
            employee_name={}
            employee = Employee.query.all()
            for a in answer:
                for e in employee:
                    if e.emp_id == a.emp_id:
                        employee_name[a.emp_id]=a.emp_username
            return render_template('question-detail.html',title='Detail',detail=question,answer=answer,employee=employee_name)
        else:
            return redirect(url_for('customer_login'))

def show_error(judge=False):
    if judge:
        return not session.get("EMPID")
    return redirect('/emp_login')


def cus_show_error(judge=False):
    if judge:
        return not session.get('CUSID')
    return redirect('/customer_login')


@app.route('/cus_mainpage________',methods=['GET','POST'])
def cus_mainpage():
    if show_error(True):
        return show_error()
    if request.method == 'GET':
        return render_template('customer-mainpage.html', title='cus_register')


@app.route('/cus_appointment', methods=['GET','POST'])
def cus_appointment():
    return render_template('customer-appointment.html', title='cus_appointment')



@app.route('/customer_mainpage', methods=['GET', 'POST'])
def customer_mainpage():
    if cus_show_error(True):
        return show_error()
    if request.method == 'GET':
        username = Customer.query.filter(Customer.cus_id == session.get('CUSID')).first()
        return render_template('customer-mainpage.html', title='Mainpage',username= username.cus_username)



