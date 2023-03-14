from website.models import Account, Transactions, Curr_Term, Term_Data, db
import website.utils.format as format
from datetime import datetime

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
    accounts = Account.query.filter_by(username=username).all()
    
    savings_accounts = []
    checkings_accounts = []

    for acc in accounts:
        if not acc.status:
            continue

        if acc.acc_type == 0:
            savings_accounts.append(acc)
        else:
            checkings_accounts.append(acc)
    
    for i in range(len(savings_accounts)):
        savings_accounts[i] = format.deep_format_acc(savings_accounts[i])

    for i in range(len(checkings_accounts)):
        checkings_accounts[i] = format.deep_format_acc(checkings_accounts[i])

    return savings_accounts, checkings_accounts

def make_withdrawal(acc_no, amt, description):
    acc = Account.query.get(acc_no)

    if not acc:
        return '0'

    amt = float(amt)

    if acc.bal - amt < acc.min_bal:
        return '1'

    term = Curr_Term.query.all()[0].term

    transaction = Transactions(acc_no=acc_no, amt=amt, start_bal=acc.bal, 
                               end_bal=acc.bal - amt, withdrawal_deposit=False,
                               description=description, term=term, 
                               date=datetime.now())

    db.session.add(transaction)

    acc.bal -= amt

    db.session.commit()

    return '2'

def make_deposit(acc_no, amt, description):
    acc = Account.query.get(acc_no)

    if not acc:
        return '0'

    amt = float(amt)

    term = Curr_Term.query.all()[0].term

    transaction = Transactions(acc_no=acc_no, amt=amt, start_bal=acc.bal, 
                               end_bal=acc.bal + amt, withdrawal_deposit=True, 
                               description=description, term=term, 
                               date=datetime.now())
    db.session.add(transaction)

    acc.bal += amt

    db.session.commit()

    return '1'

def transfer(acc_no, transfer_no, description, amt=0.0, deletion=False):
    
    # Find the account associated with the account sending money. 
    # Return error code 1 if we don't find it.
    acc = Account.query.get(acc_no)
    if not acc:
        return '0'
    
    if deletion:
        amt = acc.bal

    # Find the account associated with the account recieving money. 
    # Return error code 2 if we don't find it.
    transfer_acc = Account.query.get(transfer_no)
    if not transfer_acc:
        return '1'
    
    # Check that the usernames on both accounts match. Return error 
    # code 3 if not true.
    if acc.username != transfer_acc.username:
        return '2'

    # Get the current term.
    term = Curr_Term.query.all()[0].term

    # If we are deleting the account we skip this if, 
    # otherwise we need to do this.
    if not deletion:

        # Check if we are going to dip below the minimum balance allowed.
        if acc.bal - amt < acc.min_bal:
            return '3'

        # Add transaction object for sending account.
        transaction_from = Transactions(acc_no=acc_no, amt=-amt, 
                                        start_bal=acc.bal, 
                                        end_bal=acc.bal - amt, 
                                        withdrawal_deposit=False, 
                                        description=description, term=term)

        # Add both transaction objects to session.
        db.session.add(transaction_from)
    
    # Add transaction object for recieving account.
    transaction_to = Transactions(acc_no=transfer_no, amt=amt, 
                                    start_bal=acc.bal, 
                                    end_bal=acc.bal + amt, 
                                    withdrawal_deposit=True, 
                                    description=description, term=term)

    db.session.add(transaction_to)

    # Transfer the amount out of the account.
    acc.bal -= amt

    # Transfer the amount into the transfer account.
    transfer_acc.bal += amt

    # Caller must commit changes to confirm a valid status.

    # Success code.
    return '4'

class Account_History:

    def __init__(self, acc_no):
        curr_bal = Account.query.get(acc_no).bal

        transactions = Transactions.query.filter_by(acc_no=acc_no).all()
        
        sz = len(transactions)

        self.labels = [format.format_date_2(datetime.now())]
        self.values = [curr_bal]

        i = sz - 1

        while i >= 0:
            t = transactions[i]

            if t.withdrawal_deposit == False:
                curr_bal += t.amt
            else:
                curr_bal -= t.amt

            dt = format.format_date_2(t.date)

            self.labels.append(dt)

            self.values.append(curr_bal)

            i -= 1

        i = 0
        j = len(self.labels) - 1

        while i < j:
            self.labels[i], self.labels[j] = self.labels[j], self.labels[i]

            self.values[i], self.values[j] = self.values[j], self.values[i]

            i += 1
            j -= 1
