from healingpawsapp import db
from datetime import datetime


class Customer(db.Model):
    cus_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cus_username = db.Column(db.String(64), unique=True)
    cus_real_name = db.Column(db.String)
    email = db.Column(db.String(128), unique=True)
    cus_password_hash = db.Column(db.String(128))
    phone = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return '<Customer {}>'.format(self.cus_username)

class Employee(db.Model):
    #The information of employees
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

