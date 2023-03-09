from models import Account, Transactions, Curr_Term, Term_Data
import format
from app import db

def create_acc(username, bal = 0.0, min_bal = 0.0, acc_type = 0, ir = 0.0):
    new_acc = Account(acc_type=acc_type, username=username, ir=ir, min_bal=min_bal, bal=bal)
    db.session.add(new_acc)
    db.session.commit()

    acc_no = new_acc.acc_no
    term = Term_Data(acc_no=acc_no, term=Curr_Term.query.all()[0].term, start_bal=bal)

    db.session.add(term)
    db.session.commit()

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

def make_withdrawal(acc_no, amt, description):
    acc = Account.query.get(acc_no)

    if acc.bal - amt < acc.min_bal:
        return False

    term = Curr_Term.query.all()[0].term

    transaction = Transactions(acc_no=acc_no, amt=-amt, start_bal=acc.bal, 
                               end_bal=acc.bal - amt, withdrawal_deposit=False,
                               description=description, term=term)

    db.session.add(transaction)

    acc.bal -= amt

    db.session.commit()

def make_deposit(acc_no, amt, description):
    acc = Account.query.get(acc_no)

    term = Curr_Term.query.all()[0].term

    transaction = Transactions(acc_no=acc_no, amt=amt, start_bal=acc.bal, 
                               end_bal=acc.bal + amt, withdrawal_deposit=True, 
                               description=description, term=term)
    db.session.add(transaction)

    acc.bal += amt

    db.session.commit()

def delete_acc(acc_no):
    acc = Account.query.get(acc_no)
    
    if not acc:
        return False

    db.session.delete(acc)
    db.session.commit()

    return True

def transfer_all(acc_no, transfer_no, description):
    acc = Account.query.get(acc_no)

    if not acc:
        return False

    transfer_acc = Account.query.get(transfer_no)

    if not transfer_acc:
        return False
    
    term = Curr_Term.query.all()[0].term

    transaction_from = Transactions(acc_no=acc_no, amt=-acc.bal, start_bal=acc.bal, end_bal=0.0, withdrawal_deposit=False, description=description, term=term)
    transaction_to = Transactions(acc_no=transfer_no, amt=acc.bal, start_bal=transfer_acc.bal, end_bal=transfer_acc.bal + acc.bal, withdrawal_deposit=True, description=description, term=term)

    db.session.add(transaction_from)
    db.session.add(transaction_to)

    transfer_acc.bal += acc.bal

    acc.bal = 0.0

    db.session.commit()

def transfer(acc_no, transfer_no, amt, description):
    acc = Account.query.get(acc_no)

    if not acc:
        return False

    transfer_acc = Account.query.get(transfer_no)

    if not transfer_acc:
        return False

    if acc.bal - amt < acc.min_bal:
        return False

    term = Curr_Term.query.all()[0].term

    transaction_from = Transactions(acc_no=acc_no, amt=-amt, start_bal=acc.bal, end_bal=acc.bal - amt, withdrawal_deposit=False, description=description, term=term)
    transaction_to = Transactions(acc_no=transfer_no, amt=amt, start_bal=acc.bal, end_bal=acc.bal + amt, withdrawal_deposit=True, description=description, term=term)

    db.session.add(transaction_from)
    db.session.add(transaction_to)

    acc.bal -= amt

    transfer_acc.bal += amt

    db.session.commit()
