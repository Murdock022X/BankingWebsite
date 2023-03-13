from models import Account, Transactions, Curr_Term, Term_Data
import format
from app import db
from datetime import date

def create_acc(username, bal=0.0, min_bal=0.0, acc_type=0, apy=0.0):
    new_acc = Account(acc_type=acc_type, username=username, apy=apy, min_bal=min_bal, bal=bal)
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

    amt = float(amt)

    if acc.bal - amt < acc.min_bal:
        return False

    term = Curr_Term.query.all()[0].term

    transaction = Transactions(acc_no=acc_no, amt=-amt, start_bal=acc.bal, 
                               end_bal=acc.bal - amt, withdrawal_deposit=False,
                               description=description, term=term)

    db.session.add(transaction)

    acc.bal -= amt

    db.session.commit()

    return True

def make_deposit(acc_no, amt, description):
    acc = Account.query.get(acc_no)

    amt = float(amt)

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

    # Caller must commit this change.

    return True


def transfer(acc_no, transfer_no, description, amt=0.0, deletion=False):
    
    # Find the account associated with the account sending money. 
    # Return error code 1 if we don't find it.
    acc = Account.query.get(acc_no)
    if not acc:
        return 1
    
    if deletion:
        amt = acc.bal

    # Find the account associated with the account recieving money. 
    # Return error code 2 if we don't find it.
    transfer_acc = Account.query.get(transfer_no)
    if not transfer_acc:
        return 2
    
    # Check that the usernames on both accounts match. Return error 
    # code 3 if not true.
    if acc.username != transfer_acc.username:
        return 3

    # If we are deleting the account we skip this if, 
    # otherwise we need to do this.
    if not deletion:

        # Check if we are going to dip below the minimum balance allowed.
        if acc.bal - amt < acc.min_bal:
            return 4

        # Get the current term.
        term = Curr_Term.query.all()[0].term

        # Create transaction objects for both accounts involved.
        transaction_from = Transactions(acc_no=acc_no, amt=-amt, 
                                        start_bal=acc.bal, 
                                        end_bal=acc.bal - amt, 
                                        withdrawal_deposit=False, 
                                        description=description, term=term)
        transaction_to = Transactions(acc_no=transfer_no, amt=amt, 
                                      start_bal=acc.bal, 
                                      end_bal=acc.bal + amt, 
                                      withdrawal_deposit=True, 
                                      description=description, term=term)

        # Add both transaction objects to session.
        db.session.add(transaction_from)
        db.session.add(transaction_to)

    # Transfer the amount out of the account.
    acc.bal -= amt

    # Transfer the amount into the transfer account.
    transfer_acc.bal += amt

    # Caller must commit changes to confirm a valid status.

    # Success code.
    return 0

class Account_History:

    def __init__(self, acc_no):
        curr_bal = Account.query.get(acc_no).bal

        transactions = Transactions.query.filter_by(acc_no=acc_no).all()
        
        sz = len(transactions)

        self.labels = [format.format_date_2(date.today())]
        self.values = [curr_bal]

        for t in transactions:
            
            if t.withdrawal_deposit == False:
                curr_bal -= t.amt
            else:
                curr_bal += t.amt

            dt = format.format_date_2(t.date)

            self.labels.append(dt)

            self.values.append(curr_bal)

        i = 0
        j = len(self.labels) - 1

        while i < j:
            self.labels[i], self.labels[j] = self.labels[j], self.labels[i]

            self.values[i], self.values[j] = self.values[j], self.values[i]

            i += 1
            j -= 1


        




