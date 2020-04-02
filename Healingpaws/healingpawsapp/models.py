from healingpawsapp import db
from datetime import datetime


class Customer(db.Model):
    cus_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cus_username = db.Column(db.String(64), index=True, unique=True)
    cus_real_name = db.Column(db.String, index=True)
    email = db.Column(db.String(128), index=True, unique=True)
    cus_password_hash = db.Column(db.String(128), index=True)
    phone = db.Column(db.String(64), index=True, unique=True)
    pet = db.relationship('Pet', backref="owner", lazy="dynamic")
    question = db.relationship('QandA', backref="questioner", lazy="dynamic")
    appointment = db.relationship('Appointment', backref="booking_person", lazy="dynamic")

    def __repr__(self):
        return '<Customer {}>'.format(self.cus_username)


class Employee(db.Model):
    emp_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    emp_username = db.Column(db.String(64), index=True, unique=True)
    emp_real_name = db.Column(db.String, index=True)
    email = db.Column(db.String(128), index=True, unique=True)
    emp_password_hash = db.Column(db.String(128), index=True)
    phone = db.Column(db.String(64), index=True, unique=True)
    title = db.Column(db.Enum('0', '1', '2'), index=True, server_default='0')
    # 0 stand for normal, 1 stands for principle, 2 stands for professional
    answer = db.relationship('QandA', backref="answerer", lazy="dynamic")
    surgery = db.relationship('Surgery', backref="surgeon", lazy="dynamic")
    appointment = db.relationship('Appointment', backref="confirm_person", lazy="dynamic")
    treatment = db.relationship('Treatment', backref="treatment_person", lazy="dynamic")
    hos_id = db.Column(db.Integer, db.ForeignKey('hos_id'))

    def __repr__(self):
        return '<Employ {}>'.format(self.emp_username)


class Pet(db.Model):
    pet_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pet_name = db.Column(db.String(64), index=True)
    pet_type = db.Column(db.Enum('0', '1'), index=True, server_default='0') # 0 stand for dog, 1 stand for cat
    cus_id = db.Column(db.Integer, db.ForeignKey('cus_id'))
    app_id = db.Column(db.Integer, db.ForeignKey('app_id'))

    def __repr__(self):
        return '<Pet {}>'.format(self.pet_name)


class QandA(db.Model):
    que_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question = db.Column(db.String(128), index=True)
    answer = db.Column(db.String(128), index=True)
    que_time = db.Column(db.DateTime, index=True, default=datetime.now)
    answer_time = db.Column(db.DateTime, index=True, default=datetime.now)
    cus_id = db.Column(db.Integer, db.ForeignKey('cus_id'))
    emp_id = db.Column(db.Integer, db.ForeignKey('emp_id'))
    cus_username = db.Column(db.Integer, db.ForeignKey('cus_username'))
    emp_username = db.Column(db.Integer, db.ForeignKey('emp_username'))


class Hospital(db.Model):
    hos_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    con_num = db.Column(db.Integer, unique=True, index=True)
    principle = db.Column(db.Integer, index=True)
    place = db.Column(db.String(64), index=True)
    city = db.Column(db.String(64),index=True)
    appointment = db.relationship('Appointment', backref="hospital", lazy="dynamic")
    employee = db.relationship('Employee', backref="employee", lazy="dynamic")

class Appointment(db.Model):
    app_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    app_time = db.Column(db.DateTime, index=True, default=datetime.now)
    discription = db.Column(db.String(128), index=True)
    type = db.Column(db.Enum('0', '1'), index=True, server_default='1')
    # 0 stand for emergency, 1 stand for stander
    place = db.Column(db.String(64), db.ForeignKey('place'))
    city = db.Column(db.String(64), db.ForeignKey('city'))
    tre_id = db.Column(db.Integer, db.ForeignKey('tre_id'))
    cus_id = db.Column(db.Integer, db.ForeignKey('cus_id'))
    emp_id = db.Column(db.Integer, db.ForeignKey('emp_id'))



class Treatment(db.Model):
    tre_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tre_date = db.Column(db.DateTime, index=True, default=datetime.now)
    appointment = db.Column(db.Integer, db.ForeignKey('app_id'))
    surgery = db.Column(db.Integer, db.ForeignKey('sur_id'))
    payment = db.Column(db.Integer,index=True)
    emp_id = db.Column(db.Integer, db.ForeignKey('emp_id'))


class Surgery(db.Model):
    sur_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    surgery_time = db.Column(db.DateTime, index=True)
    complete_time = db.Column(db.DateTime, index=True)
    release_time = db.Column(db.DateTime, index=True)
    tre_id = db.Column(db.Integer, db.ForeignKey('tre_id'))
    surgeon = db.relationship('Employee', backref="executor", lazy="dynamic")
