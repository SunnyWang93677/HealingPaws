from healingpawsapp import db
from datetime import datetime


class Customer(db.Model):
    __tablename__ = 'Customer'
    cus_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cus_username = db.Column(db.String(64), unique=True)
    cus_real_name = db.Column(db.String(64))
    email = db.Column(db.String(128), unique=True)
    cus_password_hash = db.Column(db.String(128))
    phone = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return '<Customer {}>'.format(self.cus_username)


class Employee(db.Model):
    __tablename__ = 'Employee'
    emp_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    emp_username = db.Column(db.String(64), index=True, unique=True)
    emp_real_name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(128), index=True, unique=True)
    emp_password_hash = db.Column(db.String(128), index=True)
    phone = db.Column(db.String(64), index=True, unique=True)
    title = db.Column(db.Enum('0', '1', '2'), index=True, server_default='0')
    # 0 stand for normal, 1 stands for principle, 2 stands for professional
    hos_id = db.Column(db.Integer, db.ForeignKey('Place.hos_id'))
    employee_pass = db.Column(db.Enum('0', '1', '2'), server_default='0')

    # 0 waiting for pass, 1 pass, 2 not pass
    def __repr__(self):
        return '<Employ {}>'.format(self.emp_username)


class Question(db.Model):
    __tablename__ = 'Question'
    que_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    que_title = db.Column(db.String(64), index=True)
    question = db.Column(db.String(128), index=True)
    que_time = db.Column(db.DateTime, index=True, default=datetime.now)
    cus_id = db.Column(db.Integer, db.ForeignKey('Customer.cus_id'))
    customer = db.relationship('Customer', backref=db.backref('questions'), foreign_keys=[cus_id])


class Answer(db.Model):
    __tablename__ = 'Answer'
    ans_id = db.Column(db.Integer, primary_key=True, index=True, autoincrement=True)
    answer = db.Column(db.String(128), index=True)
    answer_time = db.Column(db.DateTime, index=True, default=datetime.now)
    emp_id = db.Column(db.Integer, db.ForeignKey('Employee.emp_id'))
    que_id = db.Column(db.Integer, db.ForeignKey('Question.que_id'))
    employee = db.relationship('Employee', backref=db.backref('emp_answers'), foreign_keys=[emp_id])
    question = db.relationship('Question', backref=db.backref('qus_answers'), foreign_keys=[que_id])


class Appointment(db.Model):
    __tablename__ = 'Appointment'
    app_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    app_time = db.Column(db.DateTime, index=True, default=datetime.now)
    description = db.Column(db.String(128), index=True)
    type = db.Column(db.Enum('0', '1'), index=True, server_default='1')
    # 0 stand for emergency, 1 stand for stander
    place = db.Column(db.Enum('0', '1', '2'), index=True, server_default='0')
    # 0 beijing 1 shanghai 2 chengdu
    hos_id = db.Column(db.Integer, db.ForeignKey('Place.hos_id'))
    pet_id = db.Column(db.Integer, db.ForeignKey('Pet.pet_id'))
    pets = db.relationship('Pet',backref=db.backref('petid'),foreign_keys=[pet_id])
    cus_id=db.Column(db.Integer,db.ForeignKey('Customer.cus_id'))
    customer = db.relationship('Customer',backref=db.backref('customer_appointments'),foreign_keys=[cus_id])
    status = db.Column(db.Enum('0', '1', '2', '3', '4'), index=True, default='0')
    # 0 waiting 1 treatment 2 surgery 3 release 4 finish
    treatment_time = db.Column(db.DateTime, index=True)
    release_time = db.Column(db.DateTime, index=True)
    sergery_time = db.Column(db.DateTime, index=True)


class Pet(db.Model):
    __tablename__ = 'Pet'
    pet_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pet_name = db.Column(db.String(64), index=True)
    pet_type = db.Column(db.Enum('0', '1'), index=True, server_default='0')  # 0 stand for dog, 1 stand for cat
    pet_gneger = db.Column(db.Enum('0', '1'), index=True)  # 0 for mail 1 for female
    pet_birth = db.Column(db.Date, index=True)
    pet_status = db.Column(db.Enum('0', '1'), index=True, server_default='0')  # 0 for exist 1 for delete
    cus_id = db.Column(db.Integer, db.ForeignKey('Customer.cus_id'))
    customer = db.relationship('Customer', backref=db.backref('pets'), foreign_keys=[cus_id])

    def __repr__(self):
        return '<Pet {}>'.format(self.pet_name)


class Place(db.Model):
    __tablename__ = 'Place'
    hos_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # zhe li shi integer
    discription = db.Column(db.String(128), index=True)
    place = db.Column(db.String(64), index=True)
    city = db.Column(db.Enum('0', '1', '2'), index=True)

    employee = db.relationship('Employee', backref=db.backref('work_hospital'), lazy="dynamic")
    appointment = db.relationship('Appointment', backref=db.backref('appointment_place'), lazy="dynamic")
    # 0 beijing 1 shanghai 2 chengdu


class Annoncement(db.Model):
    __tablename__ = 'Annoncement'
    ann_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ann_title = db.Column(db.String(64), index=True)
    annoncement = db.Column(db.String(128), index=True)
    ann_time = db.Column(db.DateTime, index=True, default=datetime.now)
