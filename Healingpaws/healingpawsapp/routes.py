from flask import render_template, flash, redirect, url_for, session, send_file, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from healingpawsapp import app, db
# from appdir.models import User, Post, Profile
from healingpawsapp.config import Config
from healingpawsapp.models import Customer, Employee, Question, Answer, Appointment
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
    if request.method == "GET":
        return render_template('employee_appointment.html')
    else:
        if (request.form.get("add_appointment")):
            place = request.form.get('place')
            pet_type = request.form.get('pet_type')
            description = request.form.get('description')
            status = request.form.get('status')
            appointment = Appointment(place = place, type = pet_type, description = description, status = status)
            db.session.add(appointment)
            db.session.commit()
            flash("add success")
            return redirect(url_for('employee_appointment'))
        if (request.form.get("edit_appointment")):
            place = request.form.get('place')
            pet_type = request.form.get('pet_type')
            description = request.form.get('description')
            status = request.form.get('status')
            id = request.form('app_id')
            Appointment.query.filter(id).update({'place': place, 'type': pet_type, 'description': description, 'status': status})
            db.session.commit()
            flash("edit success")
            return redirect(url_for('employee_appointment'))


@app.route('/index')
def index():
    return render_template('index.html', title='index')


@app.route('/customer_login', methods=['GET', 'POST'])
def customer_login():
    if request.method == 'GET':
        return render_template('customer_login.html', title='customer_login')
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
        return render_template('customer_register.html', title='cus_register')
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
            return render_template('question_detail.html',title='Detail',detail=question,answer=answer,employee=employee_name)
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
        return render_template('customer_mainpage.html', title='cus_register')


@app.route('/customer_appointment', methods=['GET','POST'])
def cus_appointment():
    if request.method == 'GET':
        return render_template('customer_appointment.html', title='cus_appointment')
    else:
        if request.form.get("submit")=='add':
            pet_type = request.form.get('pet_type')     #宠物类型
            city = request.form.get('place')            #城市
            type = request.form.get('type')            #手术类型
            comment = request.form.get('description')  #描述
            appointment = Appointment(place = city, type = type, description = comment)
            db.session.add(appointment)
            db.session.commit()
            flash("add success")
            return redirect(url_for('customer_appointment'))
        if request.form.get("delete_appointment"):
            app_id = request.form.get('app_id')
            Appointment.query.filter(app_id=app_id).delete()
            db.session.commit()
            flash("delete success")
            return redirect(url_for('customer_appointment'))
        if request.form.get("modify_appointment"):
            pet_type = request.form.get('pet_type')  # 宠物类型
            city = request.form.get('place')  # 城市
            type = request.form.get('type')  # 手术类型
            comment = request.form.get('description')  # 描述
            id = request.form.get('app_id')
            Appointment.query.filter(id).update({'place': city, 'type': type, 'description': comment})
            db.session.commit()
            flash("modify success")
            return redirect(url_for('customer_appointment'))



@app.route('/customer_mainpage', methods=['GET', 'POST'])
def customer_mainpage():
    if cus_show_error(True):
        return show_error()
    if request.method == 'GET':
        username = Customer.query.filter(Customer.cus_id == session.get('CUSID')).first()
        return render_template('customer_mainpage.html', title='Mainpage',username= username.cus_username)




