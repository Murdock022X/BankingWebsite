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
    apy = db.Column(db.Float)

    # Store balance
    bal = db.Column(db.Float)

    # Store minimum balance allowed
    min_bal = db.Column(db.Float)

class Bank_Settings(db.Model):
    # Store datetime of bank settings
    id = db.Column(db.Integer, primary_key=True)

    # Store savings interest rate
    savings_apy = db.Column(db.Float)
    
    # Store checkings interest rate
    checkings_apy = db.Column(db.Float)

    # Store savings minimum balance
    savings_min = db.Column(db.Float)

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

    acc_no = db.Column(db.Integer)

    amt = db.Column(db.Float)

    start_bal = db.Column(db.Float)

    end_bal = db.Column(db.Float)

    # False for withdrawal, true for deposit
    withdrawal_deposit = db.Column(db.Boolean)

    description = db.Column(db.String(1000))

    term = db.Column(db.Integer)

class Statements(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100))

    date = db.Column(db.Date)

    name = db.Column(db.String(100))
    
    path = db.Column(db.String(1000))

    term = db.Column(db.Integer)

# Table no longer useful.
#
# class Balance_Data(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#
#     acc_no = db.Column(db.Integer)
#
#     date = db.Column(db.Date)
#
#     bal = db.Column(db.Float)

class Term_Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    acc_no = db.Column(db.Integer)
    
    term = db.Column(db.Integer)

    start_bal = db.Column(db.Float)

class Curr_Term(db.Model):
    term = db.Column(db.Integer, primary_key=True)