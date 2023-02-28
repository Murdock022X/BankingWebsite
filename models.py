from app import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(UserMixin, db.Model):

    # User id for login purposes
    id = db.Column(db.Integer, primary_key=True)

    # Store username
    username = db.Column(db.String(100), unique=True)
    
    # Store password
    password = db.Column(db.String(100))
    
    # Store name
    name = db.Column(db.String(1000))

class Account(db.Model):
    # Primary key is account number
    acc_no = db.Column(db.Integer, unique=True, primary_key=True)

    # 0 -> Savings, 1 -> Checkings
    acc_type = db.Column(db.Integer)

    # Store username
    username = db.Column(db.String(100))
    
    # Store interest rate
    ir = db.Column(db.Float)

    # Store balance
    bal = db.Column(db.Float)

    # Store minimum balance allowed
    min_bal = db.Column(db.Float)

class Bank_Settings(db.Model):
    # Store datetime of bank settings
    id = db.Column(db.Integer, primary_key=True)

    # Store savings interest rate
    savings_ir = db.Column(db.Float)

    # Store savings minimum balance
    savings_min = db.Column(db.Float)

    # Store checkings interest rate
    checkings_ir = db.Column(db.Float)

    # Store checkings minimum balance
    checkings_min = db.Column(db.Float)

class Messages(db.Model):
    # Id for message
    id = db.Column(db.Integer, primary_key=True)

    date = db.Column(db.DateTime, server_default=func.now())

    # Associated username
    username = db.Column(db.String(100))

    # Content with message
    content = db.Column(db.String(5000))

class Alerts(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    date = db.Column(db.DateTime, server_default=func.now())

    content = db.Column(db.String(5000))

class Transactions(db.Model):
    transaction_no = db.Column(db.Integer, primary_key=True)

    date = db.Column(db.DateTime, server_default=func.now())

    username = db.Column(db.String(100))

    frm_acc = db.Column(db.Integer)

    to_acc = db.Column(db.Integer)

    amt = db.Column(db.Float)

class Statements(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100))

    date = db.Column(db.Date)

    name = db.Column(db.String(100))
    
    path = db.Column(db.String(1000))
    