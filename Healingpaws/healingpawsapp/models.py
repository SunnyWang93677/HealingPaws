from healingpawsapp import db
from datetime import datetime


class Customer(db.Model):
    __tablename__ = 'Customer'
    cus_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cus_username = db.Column(db.String(64), unique=True)
    cus_real_name = db.Column(db.String)
    email = db.Column(db.String(128), unique=True)
    cus_password_hash = db.Column(db.String(128))
    phone = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return '<Customer {}>'.format(self.cus_username)

class Employee(db.Model):
    __tablename__ = 'Employee'
    emp_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    emp_username = db.Column(db.String(64), index=True, unique=True)
    emp_real_name = db.Column(db.String, index=True)
    email = db.Column(db.String(128), index=True, unique=True)
    emp_password_hash = db.Column(db.String(128), index=True)
    phone = db.Column(db.String(64), index=True, unique=True)
    title = db.Column(db.Enum('0', '1', '2'), index=True, server_default='0')
    # 0 stand for normal, 1 stands for principle, 2 stands for professional


    def __repr__(self):
        return '<Employ {}>'.format(self.emp_username)


class QandA(db.Model):
    __tablename__ = 'QandA'
    que_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question = db.Column(db.String(128), index=True)
    answer = db.Column(db.String(128), index=True)
    que_time = db.Column(db.DateTime, index=True, default=datetime.now)
    answer_time = db.Column(db.DateTime, index=True)
    cus_id = db.Column(db.Integer, db.ForeignKey('Customer.cus_id'))
    emp_id = db.Column(db.Integer, db.ForeignKey('Employee.emp_id'))
    customer = db.relationship('Customer', backref = db.backref('questions'),foreign_keys = [cus_id])
    employee = db.relationship('Employee', backref = db.backref('answers'), foreign_keys = [emp_id])