from flask import render_template, flash, redirect, url_for, session, send_file, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from healingpawsapp import babel
import healingpawsapp
from healingpawsapp import app, db
from sqlalchemy import and_, or_
# from appdir.models import User, Post, Profile
from healingpawsapp.config import Config
from healingpawsapp.models import Customer, Employee, Question, Answer, Appointment, Pet, Annoncement

from flask_babel import Babel, gettext as _
from flask import request
# from healingpawsapp.config import LANGUAGES

import os
import re

aes_encrypt = healingpawsapp.AES_ENCRYPT()
app.config['UPLOAD_PHOTO'] = Config.PHOTO_UPLOAD_DIR
# app.config['LANGUAGES'] = 'en_US'
Language = "en_US"


def hello_world():
    print('hello world')
    return '你好 世界！'
app.add_template_global(hello_world,'hello_world')


# @babel.localeselector
# def get_locale():
#     locale = request.cookies.get('locale')
#     if locale is not None:
#         return locale
#     return 'en_US'
@babel.localeselector
def get_locale():
    return session.get('lang', 'en_US')
@app.route('/set-locale/<locale>')
def set_locale(locale):
    session['lang'] = locale
    return render_template('base.html')
# def set_locale(locale):
#     response = make_response(jsonify(message=_('Setting updated.')))
#     response.set_cookie('locale', locale, max_age=60 * 60 * 24 * 30)
#     return response

# @app.route('/Set-locale/<locale>')
# def set_locale(locale):
#     print(request.path)
#     session['lang'] = locale
#     return render_template('customer_mainpage.html')


@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('base.html')

def updateemp(name, tel, stat, email):
    Employee.query.filter(Employee.email == email).update(
        {'emp_username': name, 'employee_pass': '1' if stat == 'pass' else '0', 'phone': tel})
    db.session.commit()


@app.route('/manage', methods=['GET', 'POST'])
def b_employee():
    employee = Employee.query.filter(and_(Employee.email == 'boss@163.com', Employee.employee_pass == '1')).first()
    if session.get('EMPID') is not None:
        if session.get('EMPID') == employee.emp_id:
            if request.form.get('modify'):
                f = request.form
                updateemp(f.get('0'), f.get('1'), f.get('2'), f.get('3'))
                flash('success')
            return render_template('b.html',list=Employee.query.all())
        else:
            flash('you are not allowed')
            return redirect(url_for('employee_main'))
    else:
        flash('please login first')
        return redirect(url_for('employee_login'))





@app.route('/manage1', methods=['GET', 'POST'])
def b_employee1():
    if request.method == 'POST':
        if request.form.get('modify'):
            f = request.form
            updateemp(f.get('0'), f.get('1'), f.get('2'), f.get('3'))
    return render_template('b.html', list=Employee.query.all())


@app.route('/boss_main')
def boss_main():
    employee = Employee.query.filter(and_(Employee.email == 'boss@163.com', Employee.employee_pass == '1')).first()
    if session.get('EMPID') is not None:
        if session.get('EMPID') == employee.emp_id:
            return render_template('b_main.html',username=employee.emp_username)
        else:
            flash('you are not allowed')
            return redirect(url_for('employee_main'))
    else:
        flash('please login first')
        return redirect(url_for('employee_login'))


@app.route('/logout')
def logout():
    r = session.get('CUSID')
    if r:
        session.pop('CUSID')
        flash(_('Success'))
    return redirect(url_for('home'))


@app.route('/employee_login', methods=['GET', 'POST'])
def employee_login():
    if request.method == 'GET':
        return render_template('employee_login.html', title='employee_login')
    else:
        email = request.form.get('email')
        password = request.form.get('password')
        employee = Employee.query.filter(and_(Employee.email == email, Employee.employee_pass == '1')).first()
        if employee:
            if str(aes_encrypt.decrypt(employee.emp_password_hash))[2:-1] == password:
                session['EMPID'] = employee.emp_id
                if request.form.get('remember') == 1:
                    session.permanent = True
                else:
                    session.permanent = False
                    if employee.email == 'boss@163.com':
                        return redirect(url_for('boss_main'))
                    else:
                        return redirect(url_for('employee_main'))
            else:
                flash(_('Your password is incorrect, please try again'))
                return redirect(url_for('employee_login'))
        else:
            flash(_('the user is not exist, please register first OR the boss not pass your apply'))
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
        boss_email = request.form.get('bossemail')
        verified = request.form.get('pets')
        customer = Employee.query.filter(Employee.email == email).first()
        if customer:
            flash(_('This username has been registered,please login'))
            return redirect(url_for('employee_register'))
        else:
            if password != password2:
                flash(_('password has not match'))
                return redirect(url_for('employee_register'))
            else:
                if boss_email != 'boss@163.com':
                    flash(_('your verified email (boss email) is not correct'))
                    return redirect(url_for('employee_register'))
                else:
                    passw_hash = str(aes_encrypt.encrypt(password))[2:-1]
                    verified = str(aes_encrypt.encrypt(verified))[2:-1]
                    employee = Employee(emp_username=emp_username, emp_password_hash=passw_hash,
                                        emp_real_name=emp_real_name,
                                        email=email, phone=phone,verified_emp=verified)
                    db.session.add(employee)
                    db.session.commit()
                    flash(_("register success"))
                    return redirect(url_for('employee_login'))



@app.route('/employee_password', methods=['GET', 'POST'])
def employee_password():
    if request.method == 'GET':
        return render_template('employee_password.html')
    else:
        email = request.form.get('email')
        pet = request.form.get('pets')
        password = request.form.get('password')
        employee = Employee.query.filter(Employee.email == email).first()
        if employee:
            emp_verified = str(aes_encrypt.decrypt(employee.verified_emp))[2:-1]
            password_hash = str(aes_encrypt.encrypt(password))[2:-1]
            if emp_verified == pet:
                Employee.query.filter(email).update(
                    {'emp_password_hash': password_hash})
                db.session.commit()
                flash(_('update success'))
                return redirect(url_for('employee_login'))
            else:
                flash(_('verify information is not correct'))
                return redirect(url_for('employee_password'))
        else:
            flash(_('the email is not exist, please register first'))
            return redirect(url_for('employee_password'))



@app.route('/employee', methods=['GET', 'POST'])
def employee():
    return render_template('employee.html')


@app.route('/employee_main', methods=['GET', 'POST'])
def employee_main():
    if session.get('EMPID'):
        announcemnet = Annoncement.query.first()
        print(announcemnet.ann_title)
        employee = Employee.query.filter(Employee.emp_id == int(session.get('EMPID'))).first()
        if announcemnet:
            print('hello word announcement')
            return render_template('employee_main.html',username=employee.emp_username,announcement_title=announcemnet.ann_title,announcement_connect=announcemnet.annoncement,announcement_time=announcemnet.ann_time )
        else:
            return render_template('employee_main.html',username=employee.emp_username )
    else:
        flash('please login first')
        return redirect(url_for('employee_login'))


@app.route('/employee_question', methods=['GET', 'POST'])
def employee_qa():
    if request.method == 'GET':
        if session.get('EMPID'):
            employee = Employee.query.filter(Employee.emp_id == int(session.get('EMPID'))).first()
            questions = Question.query.all()
            return render_template('employee_question.html', questions=questions,username=employee.emp_username)
        elif session.get('EMPID') is None:
            flash(_('please login first'))
            return redirect(url_for('employee_login'))

        elif session.get('CUSID'):
            flash(_('Limit Enter'))
            return redirect(url_for('cus_mainpage'))
        else:
            return redirect(url_for('customer_login'))



@app.route('/employee_question/<que_id>', methods=['GET', 'POST'])
def answer_detial(que_id):
    if request.method == 'GET':
        if session.get('EMPID'):
            employee_username = Employee.query.filter(Employee.emp_id == int(session.get('EMPID'))).first()
            question = Question.query.filter(Question.que_id == que_id).first()
            answer = Answer.query.filter(Answer.que_id == que_id).all()
            customer = Customer.query.filter(Customer.cus_id == question.cus_id).first()
            employee_name = {}
            employee = Employee.query.all()
            for a in answer:
                for e in employee:
                    if e.emp_id == a.emp_id:
                        employee_name[a.emp_id] = e.emp_username
            return render_template('answer_detail.html', title='Detail', detail=question, answer=answer,
                                   employee=employee_name, customer=customer,username=employee_username)
        else:
            flash(_('please login'))
            return redirect(url_for('employee_login'))
    else:
        if session.get('EMPID'):
            answer = request.form.get('answer')
            if answer is not None:
                ans_detail = Answer(answer=answer, emp_id=session.get('EMPID'), que_id=que_id)
                db.session.add(ans_detail)
                db.session.commit()
                flash(_('add success'))
            else:
                flash(_('please enter something'))
            return redirect(url_for('answer_detial', que_id=que_id))


@app.route('/employee_appointment', methods=['GET', 'POST'])
def employee_appointment():
    if request.method == "GET":
        if session.get('EMPID'):
            employee_username = Employee.query.filter(Employee.emp_id == int(session.get('EMPID'))).first()
            appointment = Appointment.query.all()
            pets = Pet.query.all()
            customers = Customer.query.all()
            customer={}
            pet={}
            for a in appointment:
                for c in customers:
                    if a.cus_id == c.cus_id:
                        customer[c.cus_id]=c
                for p in pets:
                    if a.pet_id == p.pet_id:
                        pet[p.pet_id]=p
            return render_template('employee_appointment.html', appointment=appointment,pet_name_list=pet,customer=customer,username=employee_username)
        else:
            flash(_('Please login as Employee first'))
            return redirect(url_for('employee_login'))
    else:
        if request.form.get("update_appointment") == "1":
            app_id=request.form.get('pid')
            status = request.form.get('place')
            treatment_time = request.form.get('treatment_time1')
            surgery_time = request.form.get('surgery_time1')
            release_time = request.form.get('release_time1')

            Appointment.query.filter(Appointment.app_id == app_id).update(
                {'status': status, 'treatment_time': treatment_time, 'sergery_time': surgery_time, 'release_time': release_time})
            db.session.commit()
            flash(_("edit success"))
            return redirect(url_for('employee_appointment'))


@app.route('/announcement', methods=['GET','POST'])
def announcement():
    employee = Employee.query.filter(and_(Employee.email == 'boss@163.com', Employee.employee_pass == '1')).first()
    if request.method == 'GET':
        if session.get('EMPID') is not None:
            if session.get('EMPID') == employee.emp_id:
                flash(_('success'))
                return render_template('announcement.html')
            else:
                flash(_('forbidden enter'))
                return redirect(url_for('employee_main'))
        else:
            flash(_('Please login first'))
            return redirect(url_for('employee_login'))
    else:
        title = request.form.get('title')
        conntent = request.form.get('conntent')
        announcement = Annoncement(ann_title=title,annoncement=conntent)
        db.session.add(announcement)
        db.session.commit()
        flash(_('add success'))
    return render_template('announcement.html')


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
        if (email is not None) and (password is not None):
            customer = Customer.query.filter(Customer.email == email).first()
            if customer:
                if str(aes_encrypt.decrypt(customer.cus_password_hash))[2:-1] == password:
                    session['CUSID'] = str(customer.cus_id) + 'CUS'
                    if request.form.get('remember') == 1:
                        session.permanent = True
                    else:
                        session.permanent = False
                    flash('success')
                    return redirect(url_for('customer_mainpage'))
                else:
                    flash(_('Your password is incorrect, please try again'))
                    return redirect(url_for('customer_login'))
            else:
                flash(_('the user is not exist, please register first'))
                return redirect(url_for('customer_login'))
        else:
            flash(_('password or email empty'))
            return redirect(url_for('customer_login'))


@app.route('/ttt', methods=['GET', 'POST'])
def tanchuang():
    if request.method == 'POST':
        print(request.form.get('aa'))
        if (request.form.get('aa') == '123456'):
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
        verified = request.form.get('question')
        customer_db = Customer.query.filter(Customer.email == email or Customer.phone == phone).first()
        if customer_db:
            flash(_('This email or phone has been registered'))
            return redirect(url_for('customer_register'))
        else:
            if cus_password != cus_password_2:
                flash(_('password has not match'))
                return redirect(url_for('customer_register'))
            else:
                cus_password_hash = str(aes_encrypt.encrypt(cus_password))[2:-1]
                verified = str(aes_encrypt.encrypt(verified))[2:-1]
                customer = Customer(cus_username=cus_username, cus_password_hash=cus_password_hash,
                                    cus_real_name=cus_real_name,
                                    email=email, phone=phone,verified_cus=verified)
                db.session.add(customer)
                db.session.commit()
                flash(_('scuess'))
                return redirect(url_for('customer_login'))



@app.route('/customer_password', methods=['GET', 'POST'])
def customer_password():
    if request.method == 'GET':
        return render_template('customer_resetpsw.html')
    else:
        email = request.form.get('email')
        pet = request.form.get('answer')
        password = request.form.get('question')
        customer = Customer.query.filter(Customer.email == email).first()
        if customer:
            cus_verified = str(aes_encrypt.decrypt(customer.verified_cus))[2:-1]
            password_hash = str(aes_encrypt.encrypt(password))[2:-1]
            if cus_verified == pet:
                Customer.query.filter(email).update(
                    {'emp_password_hash': password_hash})
                db.session.commit()
                flash(_('update success'))
                return redirect(url_for('customer_login'))
            else:
                flash(_('verify information is not correct'))
                return redirect(url_for('customer_password'))
        else:
            flash(_('the email is not exist, please register first'))
            return redirect(url_for('customer_password'))



@app.route('/customer_question', methods=['GET', 'POST'])
def customer_question():
    if request.method == 'GET':
        if session.get('CUSID'):
            cusid = int(session.get('CUSID')[:-3])
            data = Question.query.filter(and_(Question.cus_id == cusid, Question.que_status == '0')).all()
            question = Question.query.all()
            # flash('nothing over here')
            customer = Customer.query.filter(Customer.cus_id == cusid).first()
            return render_template('customer_question.html', title='Question', questionlist=data, question=question,username=customer.cus_username)

        else:
            return redirect(url_for('customer_login'))
    else:
        if session.get('CUSID'):
            title = request.form.get('title')
            question = request.form.get('comment')
            if (title and question) is not None:
                data = Question(que_title=title, question=question, cus_id=int(session.get('CUSID')[:-3]))
                db.session.add(data)
                db.session.commit()
            else:
                flash(_('please enter something'))
            print('delete_confirm', request.form.get('delete_confirm'))
            if request.form.get('delete_confirm'):
                id = request.form.get('question_id')
                print(id)
                # data = Question.query.filter(Question.que_id == id).first()
                Question.query.filter_by(que_id=id).update(
                    {'que_status': '1'})
                db.session.commit()
                flash(_('success'))
            return redirect(url_for('customer_question'))
        else:
            flash(_('please login first'))
            return redirect(url_for('customer_login'))


@app.route('/customer_question/<que_id>', methods=['GET', 'POST'])
def detail(que_id):
    if request.method == 'GET':
        if session.get('CUSID'):
            Username = Customer.query.filter(Customer.cus_id == int(session.get('CUSID')[:-3])).first()
            question = Question.query.filter(Question.que_id == que_id).first()
            answer = Answer.query.filter(Answer.que_id == que_id).all()
            customer = Customer.query.filter(Customer.cus_id == question.cus_id).first()
            employee_name = {}
            employee = Employee.query.all()
            for a in answer:
                for e in employee:
                    if e.emp_id == a.emp_id:
                        employee_name[a.emp_id] = e.emp_username
            return render_template('question_detail.html', title='Detail', customer=customer, detail=question,
                                   answer=answer, employee=employee_name,username = customer.cus_username,Username=Username.cus_username)
        else:
            flash(_('Please login first'))
            return redirect(url_for('customer_login'))



def get_pet_list(id):
    # return a list of all the pets. This function will send request to MySQL database
    pet = Pet.query.filter(and_(Pet.pet_status == '0', Pet.cus_id == id)).all()
    return pet


def add_new_pet(cus_id):
    p = Pet(pet_name='pet name', pet_type='0', pet_gneger='0', pet_birth='2020-03-05', cus_id=cus_id)
    db.session.add(p)
    db.session.commit()
    return p


def update_pet_db(id, na, ty, ge, bi):
    Pet.query.filter_by(pet_id=id).update({'pet_name': na, 'pet_gneger': ge, 'pet_birth': bi, 'pet_type': ty})
    db.session.commit()


def delete_pet(id):
    Pet.query.filter_by(pet_id=id).update({'pet_status': '1'})
    db.session.commit()


def g(s):
    return request.form.get(s)


@app.route('/pet', methods=['GET', 'POST'])
def pet_page():
    if session.get('CUSID'):
        if request.method == "POST":
            print(request.form)
            if request.form.get('update'):
                update_pet_db(g('pid'), g('petname'), g('pkind'), g('pgender'), g('birthday'))
                flash(_('Success'))
            if request.form.get('delete'):
                delete_pet(g('pid'))
                flash(_('Success'))
            if request.form.get('add_pet'):
                add_new_pet(int(session.get('CUSID')[:-3]))
        petsList = get_pet_list(int(session.get('CUSID')[:-3]))
        customer = Customer.query.filter(Customer.cus_id == int(session.get('CUSID')[:-3])).first()
        return render_template('customer_pet.html', pet=[], pets=petsList,username=customer.cus_username)
    else:
        flash(_('Please login first'))
        return redirect('/customer_login')


@app.route('/pet_bad', methods=['GET', 'POST'])
def pet_bad():
    print(request.form)
    # return render_template('customer_pet.html', pet=[])
    if session.get('CUSID') is not None:
        if request.method == 'GET':
            pets = Pet.query.filter(Pet.cus_id == int(session.get('CUSID')[:-3]))
            print(pets)
            return render_template('customer_pet.html', pet=pets)
        else:
            if request.form.get('submit') is not None:
                petid = request.form.get('pet_id')
                pet_type = request.form.get('petkind')
                pet_gender = request.form.get('petgender')
                pet_name = request.form.get('petname')
                pet_birthday = request.form.get('birthday')
                pet = Pet.query.filer(Pet.pet_id == petid).first()
                if pet is not None:
                    Pet.query.filter_by(pet_id=petid).update({
                        'pet_name': pet_name, 'pet_type': pet_type, 'pet_genger': pet_gender, 'pet_birth': pet_birthday
                    })
                    db.session.commit()
                else:
                    flash(_('pets not exist'))
            if request.form.get('delete_confirm') is not None:
                petid = request.form.get('petid_delete')
                Pet.query.filter_by(pet_id=petid).update({
                    'pet_status': '1'
                })
                db.session.commit()
            if request.form.get('add_pet') is not None:
                pet_type = request.form.get('petkind')
                pet_gender = request.form.get('petgender')
                pet_name = request.form.get('petname')
                pet_birthday = request.form.get('birthday')
                pet = Pet(pet_name=pet_name, pet_type=pet_type, pet_gneger=pet_gender, pet_birth=pet_birthday,
                          cus_id=int(session.get('CUSID')[:-3]))
                db.session.add(pet)
                db.session.commit()
            pets = Pet.query.filter(Pet.cus_id == int(session.get('CUSID')[:-3]))
            return render_template('customer_pet.html', pet=pets)
    else:
        flash(_('please login first'))
        redirect(url_for('customer_login'))


def show_error(judge=False):
    if judge:
        return not session.get("EMPID")
    return redirect('/emp_login')


def cus_show_error(judge=False):
    if judge:
        return not session.get('CUSID')
    return redirect('/customer_login')


@app.route('/cus_mainpage________', methods=['GET', 'POST'])
def cus_mainpage():
    if show_error(True):
        return show_error()
    if request.method == 'GET':
        return render_template('customer_mainpage.html', title='cus_register')


@app.route('/customer_appointment', methods=['GET', 'POST'])
def customer_appointment():
    if session.get('CUSID'):
        if request.method == 'GET':
            customer=Customer.query.filter(Customer.cus_id == int(session.get('CUSID')[:-3])).first()
            appointment = Appointment.query.filter(Appointment.cus_id == int(session.get('CUSID')[:-3])).all()
            # this one is empty
            pet = Pet.query.filter(and_(Pet.cus_id == int(session.get('CUSID')[:-3]),Pet.pet_status == '0')).all()
            appointment_pet = {}
            for p in pet:
                for a in appointment:
                    if p.pet_id == a.pet_id:
                        appointment_pet[p.pet_id] = p.pet_name
            return render_template('customer_appointment.html', appointment=appointment, title='cus_appointment',
                                   appointment_pet=appointment_pet, pet=pet,username=customer.cus_username)
        else:
            print(request.form)
            if request.form.get('update_appointment'):
                print('current update')
                myid = int(request.form.get('pid'))
                update_appoint(myid, request.form.get('eon'), request.form.get('place'),
                               request.form.get('treatment_time'), request.form.get('description'))
                flash(_('Modify success'))
            elif request.form.get('delete_appointment'):
                id = int(request.form.get('app_id'))
                Appointment.query.filter_by(app_id=id).update({'status': '5'})
                db.session.commit()
                flash(_('Delete success'))
            else:
                a = Appointment(description=request.form.get('description'), type=request.form.get('type'),
                                place=request.form.get('place'), pet_id=request.form.get('petid'),
                                cus_id=int(session.get('CUSID')[:-3]),
                                treatment_time=request.form.get('treatment_time'))
                db.session.add(a)
                db.session.commit()
                flash(_('Add success'))
            # request_appointment(request.form)
            return redirect(url_for('customer_appointment'))

    else:
        flash(_('Please login first'))
        return redirect(url_for('customer_login'))


def update_appoint(id, t, city, date, comment):
    print(date)
    if comment is not None:
        Appointment.query.filter_by(app_id=id).update(
        {'type': t, 'place': city, 'treatment_time': date, 'description': comment})
        db.session.commit()
    else:
        Appointment.query.filter_by(app_id=id).update(
            {'type': t, 'place': city, 'treatment_time': date})
        db.session.commit()


def request_appointment(form):
    if form.get("add_appointment") == '1':
        print(2000)
        pet_type = form.get('pet_type')
        place = form.get('place')  # 城市
        if form.get('type') == "0":
            type = "0"
        else:
            type = "1"
        description = form.get('description')  # 描述
        date = form.get('treatment_time')
        cus_id = "1"
        appointment = Appointment(place=place, type=type, description=description, treatment_time=date, cus_id=cus_id)
        # pet = Pet(pet_type=pet_type,cus_id=cus_id)
        db.session.add(appointment)
        # db.session.add(pet)
        db.session.commit()
        flash(_("add success"))

    if form.get("delete_appointment") == "1":
        print("yes")
        app_id = form.get('app_id')
        Appointment.query.filter_by(app_id=app_id).update({'status': '1'})
        db.session.commit()

    if form.get("modify_appointment") == "1":
        print("ok")
        app_id = form.get('app_id')

    if form.get("update_appointment") == "1":
        app_id = form.get('app_id1')
        print(app_id, 'update_appointment')
        place = form.get('place')  # 城市
        if form.get('type1') == "1":
            type = "0"  # 手术类型
        else:
            type = "1"
        description = form.get('description')  # 描述
        date = form.get('treatment_time')
        cus_id = "1"
        Appointment.query.filter(app_id == app_id).update(
            {'place': place, 'type': type, 'description': description, 'treatment_time': date})
        db.session.commit()


def getAppointment(app_id):
    return Appointment.query.filter(app_id == app_id).first()


def getPet(pet_id):
    return Pet.query.filter(pet_id == pet_id).first()


def getCusAppointment(cus_id):  # 得到顾客的订单
    pets = getCustomerPets(cus_id)
    all = []
    for p in pets:
        all.append(getPetsAppointment(p.pet_id))
    return all


def getCusAppointmentById(cus_id):
    appointment = Appointment.query.filter_by(cus_id=cus_id).all()
    all = []
    for a in appointment:
        if a.cus_id == cus_id:
            all.append(a)
    return all


def getPetsAppointment(pet_id):  # 得到每个宠物的订单
    appointment = Appointment.query.filter_by(pet_id=pet_id).all()
    for a in appointment:
        if a.pet_id == pet_id:
            return a
    return None


def getCustomerPets(cus_id):  # 得到顾客的宠物
    return Pet.query.filter_by(cus_id=cus_id).all()


def getCustomer(cus_id):
    customer = Customer.query.filter_by(cus_id=cus_id).all()
    for u in customer:
        if u.cus_id == cus_id:
            return u
    return None


@app.route('/customer_mainpage', methods=['GET', 'POST'])
def customer_mainpage():
    if cus_show_error(True):
        return show_error()
    if request.method == 'GET':
        username = Customer.query.filter(Customer.cus_id == int(session.get('CUSID')[:-3])).first()
        return render_template('customer_mainpage.html', title='Mainpage', username=username.cus_username)
