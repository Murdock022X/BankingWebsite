from models import Account
import format
from app import db

def get_accounts_user(username):
    return Account.query.filter_by(username=username)

def get_account(acc_no):
    return Account.query.get(acc_no)

def checkings_savings_retrieval(username):
    accounts = Account.query.filter_by(username=username)
    res = []

    for acc in accounts:
        res.append(format.deep_format_acc(acc))

    savings_accounts = []
    checkings_accounts = []

    for acc in res:
        if acc['acc_type'] == 'Savings':
            savings_accounts.append(acc)
        else:
            checkings_accounts.append(acc)

    return savings_accounts, checkings_accounts

def make_withdrawal(acc_no, amt):
    print(acc_no, amt)
    acc = Account.query.get(acc_no)

    if acc.bal - amt < acc.min_bal:
        return False

    acc.bal -= amt

    db.session.commit()

    return True

def make_deposit(acc_no, amt):
    acc = Account.query.get(acc_no)

    acc.bal += amt

    db.session.commit()

    return True

def delete_acc(acc_no):
    acc = Account.query.get(acc_no)
    
    if not acc:
        return False

    db.session.delete(acc)
    db.session.commit()

    return True

def transfer_all(acc_no, transfer_no):
    acc = Account.query.get(acc_no)

    if not acc:
        return False

    transfer_acc = Account.query.get(transfer_no)

    if not transfer_acc:
        return False

    transfer_acc.bal += acc.bal

    acc.bal = 0.0

    db.session.commit()

    return True

