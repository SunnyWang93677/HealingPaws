from flask import render_template, flash, redirect, url_for, session, send_file, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from healingpawsapp import app, db
# from appdir.models import User, Post, Profile
from healingpawsapp.config import Config
from healingpawsapp.models import Customer, Employee, Question, Answer, Appointment, Pet


app.config['UPLOAD_PHOTO'] = Config.PHOTO_UPLOAD_DIR


@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('base.html')

@app.route('/manage', methods=['GET','POST'])
def b_employee1():
    employee = Employee.query.filter(Employee.email == 'boss@163.com' and Employee.employee_pass == '1').first()
    if session.get('EMPID') is not None:
        if session.get('EMPID') == employee.emp_id:
            return render_template('b.html')
        else:
            return redirect(url_for('employee_main'))


@app.route('/manage1', methods=['GET','POST'])
def b_employee():
        return render_template('b.html')


@app.route('/boss_main')
def boss_main():
    employee = Employee.query.filter(Employee.email == 'boss@163.com' and Employee.employee_pass == '1').first()
    if session.get('EMPID') is not None:
        if session.get('EMPID') == employee.emp_id:
            return render_template('b_main.html')
        else:
            return redirect(url_for('employee_main'))

@app.route('/logout')
def logout():
    r=session.get('CUSID')
    if r:
        session.pop('CUSID')
        flash('Success')
    return redirect(url_for('employee_login'))

@app.route('/employee_login', methods=['GET', 'POST'])
def employee_login():
    if request.method == 'GET':
        return render_template('employee_login.html', title='employee_login')
    else:
        email = request.form.get('email')
        password = request.form.get('password')
        print(email, password)
        employee = Employee.query.filter(Employee.email == email and Employee.employee_pass == '1').first()
        if employee:
            if check_password_hash(employee.emp_password_hash, password):
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
                employee = Employee(emp_username=emp_username, emp_password_hash=passw_hash,
                                    emp_real_name=emp_real_name,
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


@app.route('/employee_question', methods=['GET', 'POST'])
def employee_qa():
    if request.method == 'GET':
        if session.get('EMPID'):
            questions = Question.query.all()
            return render_template('employee_question.html', questions=questions)
        if session.get('CUSID'):
            flash('Limit Enter')
            return redirect(url_for('cus_mainpage'))
    else:
        return ''


@app.route('/employee_question/<que_id>', methods=['GET', 'POST'])
def answer_detial(que_id):
    if request.method == 'GET':
        if session.get('EMPID'):
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
                                   employee=employee_name, customer=customer)
        else:
            print('please login')
            return redirect(url_for('customer_login'))
    else:
        if session.get('EMPID'):
            answer = request.form.get('answer')
            if answer is not None:
                ans_detail = Answer(answer=answer, emp_id=session.get('EMPID'), que_id=que_id)
                db.session.add(ans_detail)
                db.session.commit()
                flash('add success')
            else:
                flash('please enter something')
            return redirect(url_for('answer_detial', que_id=que_id))


@app.route('/employee_appointment', methods=['GET', 'POST'])
def employee_ap():
    if request.method == "GET":
        #return render_template('employee_appointment.html')
        all_appointment = getAllAppointment()
        emp_appointment = []
        for a in all_appointment:
            city = a.place
            pet_name = getPet(session.get('pet_id')).pet_name
            tel = getCustomer(session.get('cus_id')).phone
            des = a.description
            pet_type = getPet(session.get('pet_id')).pet_type
            sergery_time = a.sergery_time
            release_time = a.release_time
            status = a.status
            appointment = [city, pet_name, tel, des, pet_type, sergery_time, release_time, status]
            emp_appointment.append(appointment)
        print(emp_appointment)
        return render_template('employee_appointment.html')
    else:
        if (request.form.get("add_appointment")):
            place = request.form.get('place')
            pet_type = request.form.get('pet_type')
            description = request.form.get('description')
            status = request.form.get('status')
            appointment = Appointment(place=place, type=pet_type, description=description, status=status)
            db.session.add(appointment)
            db.session.commit()
            return redirect(url_for('employee_appointment'))
        if (request.form.get("edit_appointment")):
            place = request.form.get('place')
            pet_type = request.form.get('pet_type')
            description = request.form.get('description')
            status = request.form.get('status')
            id = request.form.get('app_id')
            Appointment.query.filter(id).update(
                {'place': place, 'type': pet_type, 'description': description, 'status': status})
            db.session.commit()
            flash("edit success")
            return redirect(url_for('employee_appointment'))


def getCustomer(cus_id):
    customer = Customer.query.all()
    for cus in customer:
        if cus.cus_id == cus_id:
            return cus
    return None


def getAllAppointment():
    return Appointment.query.all()


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
        print(email, '++', password)
        if (email is not None) and (password is not None):
            customer = Customer.query.filter(Customer.email == email).first()
            if customer:
                if check_password_hash(customer.cus_password_hash, password):
                    session['CUSID'] = str(customer.cus_id) + 'CUS'
                    print("Session['CUSID']", session.get('CUSID'))
                    print("SESSION['CUSID'][:-3]", session.get('CUSID')[:-3])
                    if request.form.get('remember') == 1:
                        session.permanent = True
                    else:
                        session.permanent = False
                    return redirect(url_for('customer_mainpage'))
                else:
                    print('Your password is incorrect, please try again')
                    return redirect(url_for('customer_login'))
            else:
                print('the user is not exist, please register first')
                return redirect(url_for('customer_login'))
        else:
            return ''


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


@app.route('/customer_question', methods=['GET', 'POST'])
def customer_question():
    if request.method == 'GET':
        print(session.get('CUSID')[:-3])
        if session.get('CUSID'):
            cusid = int(session.get('CUSID')[:-3])
            data = Question.query.filter(Question.cus_id == cusid).all()
            print('nothing over here')
            return render_template('customer_question.html', title='Question', questionlist=data)

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
                flash('please enter something')
            return redirect(url_for('customer_question'))
        else:
            return redirect(url_for('customer_login'))


@app.route('/customer_question/<que_id>', methods=['GET', 'POST'])
def detail(que_id):
    if request.method == 'GET':
        if session.get('CUSID'):
            question = Question.query.filter(Question.que_id == que_id).first()
            answer = Answer.query.filter(Answer.que_id == que_id).all()
            customer = Customer.query.filter(Customer.cus_id == question.cus_id)
            employee_name = {}
            employee = Employee.query.all()
            for a in answer:
                for e in employee:
                    if e.emp_id == a.emp_id:
                        employee_name[a.emp_id] = e.emp_username
            return render_template('question_detail.html', title='Detail', customer=customer, detail=question,
                                   answer=answer, employee=employee_name)
        else:
            return redirect(url_for('customer_login'))


def get_pet_list():
    #return a list of all the pets. This function will send request to MySQL database
    pet = Pet.query.filter(Pet.pet_status == '0').all()
    return pet

def add_new_pet(cus_id):
    p = Pet(pet_name='pet name', pet_type='0', pet_gneger='0', pet_birth='2020-03-05',cus_id=cus_id)
    db.session.add(p)
    db.session.commit()
    return p

def update_pet_db(id,na,ty,ge,bi):
    Pet.query.filter_by(pet_id=id).update({'pet_name':na,'pet_gneger':ge,'pet_birth':bi,'pet_type':ty})
    db.session.commit()

def delete_pet(id):
    Pet.query.filter_by(pet_id=id).update({'pet_status':'1'})
    db.session.commit()


def g(s):
    return request.form.get(s)


@app.route('/pet',methods=['GET','POST'])
def pet_page():
    if session.get('CUSID'):
        if request.method=="POST":
            print(request.form)
            if request.form.get('update'):
                update_pet_db(g('pid'),g('petname'),g('pkind'),g('pgender'),g('birthday'))
            if request.form.get('delete'):
                delete_pet(g('pid'))
            if request.form.get('add_pet'):
                add_new_pet(int(session.get('CUSID')[:-3]))
        petsList=get_pet_list()
        return render_template('customer_pet.html',pet=[], pets=petsList)
    else:
        return redirect('/customer_login')

@app.route('/pet_bad', methods=['GET', 'POST'])
def pet_bad():
    print(request.form)
    #return render_template('customer_pet.html', pet=[])
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
                    flash('pets not exist')
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
                pet = Pet(pet_name=pet_name,pet_type=pet_type,pet_gneger=pet_gender,pet_birth=pet_birthday,cus_id=int(session.get('CUSID')[:-3]))
                db.session.add(pet)
                db.session.commit()
            pets = Pet.query.filter(Pet.cus_id == int(session.get('CUSID')[:-3]))
            return render_template('customer_pet.html', pet=pets)
    else:
        flash('please login first')
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
def cus_appointment():
    if session.get('CUSID'):
        if request.method == 'GET':
            cus_appointment = getCusAppointment(int(session.get('CUSID')[:-3]))
            all_appointment = {}
            for a in cus_appointment:
                pet_name = getPet(a.app_id).pet_name
                all_appointment[a.app_id] = pet_name
            return render_template('customer_appointment.html', name=all_appointment, all_appointment=all_appointment,
                                   title='cus_appointment')
        else:
            request.get_data()
            if request.form.get("add_appointment"):
                pet_type = request.form.get('pet_type')
                city = request.form.get('place')  # 城市
                type = request.form.get('type')  # 手术类型
                comment = request.form.get('description')  # 描述
                date = request.form.get('treatment_time')
                status = "0"
                appointment = Appointment(place=city, type=type, description=comment, treatment_time=date,
                                          status=status)
                pet = Pet(pet_type=pet_type)
                db.session.add(appointment)
                db.session.add(pet)
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
                date = request.form.get('treatment_time')
                id = request.form.get('app_id')
                Appointment.query.filter(id).update(
                    {'place': city, 'type': type, 'description': comment, 'treatment_time': date})
                db.session.commit()
                flash("modify success")
                return redirect(url_for('customer_appointment'))


def getPet(pet_id):
    pet = Pet.query.filter(Pet.pet_id == pet_id).first()
    return pet


def getCusAppointment(cus_id):  # 得到顾客的订单
    pets = getCustomerPets(cus_id)
    all = []
    for p in pets:
        all += getPetsAppointment(p.pet_id)
    return all


def getPetsAppointment(pet_id):  # 得到每个宠物的订单
    return Appointment.query.filter(Appointment.pet_id == pet_id).all()


def getCustomerPets(cus_id):  # 得到顾客的宠物
    return Pet.query.filter(Pet.cus_id == cus_id).all()


def getCustomer(cus_id):
    customer = Customer.query.filter(Customer.cus_id == cus_id).first()
    return customer


@app.route('/customer_mainpage', methods=['GET', 'POST'])
def customer_mainpage():
    if cus_show_error(True):
        return show_error()
    if request.method == 'GET':
        username = Customer.query.filter(Customer.cus_id == int(session.get('CUSID')[:-3])).first()
        return render_template('customer_mainpage.html', title='Mainpage', username=username.cus_username)
