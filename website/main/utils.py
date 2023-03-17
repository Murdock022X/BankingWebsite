from website.models import Account, Transactions, Curr_Term, Term_Data, db
import website.utils.format as format
from datetime import datetime
from wtforms.validators import ValidationError
from flask import current_app, redirect, url_for
from website.utils.flash_codes import flash_codes
from functools import wraps
from flask_login import current_user

def create_acc(username, bal=0.0, min_bal=0.0, acc_type=0, apy=0.0):
    """Create an account.

    Args:
        username (str): The username to associate with the account.
        bal (float, optional): The balance to be initialized with. 
        Defaults to 0.0.
        min_bal (float, optional): The minimum balance to be initialized with. 
        Defaults to 0.0.
        acc_type (int, optional): The type of account to make this. 
        Defaults to 0.
        apy (float, optional): The apy to be initialized for this account. 
        Defaults to 0.0.
    """    

    new_acc = Account(acc_type=acc_type, username=username, apy=apy, min_bal=min_bal, bal=bal)
    db.session.add(new_acc)
    db.session.commit()

    acc_no = new_acc.acc_no
    term = Term_Data(acc_no=acc_no, term=Curr_Term.query.all()[0].term, start_bal=bal)

    db.session.add(term)
    
    db.session.commit()


def checkings_savings_retrieval(username):
    """Return a tuple of savings and checkings accounts.

    Args:
        username (str): The username to get accounts for.

    Returns:
        tuple: A tuple of lists of savings and checkings accounts. 
    """    

    # Get all accounts associated with username.
    accounts = Account.query.filter_by(username=username).all()    
    savings_accounts = []
    checkings_accounts = []

    # Iterate through account seperating them into savings and 
    # checkings and formatting their values at the same time.
    for acc in accounts:
        if not acc.status:
            continue

        if acc.acc_type == 0:
            savings_accounts.append(format.deep_format_acc(acc))
        else:
            checkings_accounts.append(format.deep_format_acc(acc))

    return savings_accounts, checkings_accounts

def make_withdrawal(acc_no, amt, description):
    """Make a withdrawal from an account for a given amount.

    Args:
        acc_no (int): The account number to deposit to.
        amt (DecimalField): The amount to deposit.
        description (str): The descriptor for the deposit.

    Returns:
        str: The char code for the return.
    """    

    # Check account exists.
    acc = Account.query.get(acc_no)
    if not acc:
        return '0'

    # Convert decimal field to float.
    amt = float(amt)

    # Check withdrawal would not leave account below minimum balance.
    if acc.bal - amt < acc.min_bal:
        return '1'

    term = Curr_Term.query.all()[0].term

    # Create a transaction object to store history.
    transaction = Transactions(acc_no=acc_no, amt=amt, start_bal=acc.bal, 
                               end_bal=acc.bal - amt, withdrawal_deposit=False,
                               description=description, term=term, 
                               date=datetime.now())

    db.session.add(transaction)

    # Remove amount from balance.
    acc.bal -= amt

    db.session.commit()

    # Return status code.
    return '2'

def make_deposit(acc_no, amt, description):
    """Make a deposit into an account for a given amount.

    Args:
        acc_no (int): The account number to deposit to.
        amt (DecimalField): The amount to deposit.
        description (str): The descriptor for the deposit.

    Returns:
        str: The char code for the return.
    """    

    acc = Account.query.get(acc_no)

    # Return a '0' status code if the account does not exist.
    if not acc:
        return '0'

    # Convert to float.
    amt = float(amt)

    term = Curr_Term.query.all()[0].term

    # Create a transaction object to record this transaction.
    transaction = Transactions(acc_no=acc_no, amt=amt, start_bal=acc.bal, 
                               end_bal=acc.bal + amt, withdrawal_deposit=True, 
                               description=description, term=term, 
                               date=datetime.now())
    
    db.session.add(transaction)

    # Add amount to account.
    acc.bal += amt

    db.session.commit()

    # Return success code.
    return '1'

def transfer(acc_no, transfer_no, description, amt=0.0, deletion=False, 
             app=current_app):
    """Because there are so many different status indicators for this function 
    that result in different flash messages this is one of few functions where 
    we call the flash code from the util function rather than the route for 
    the page.

    Args:
        acc_no (_type_): _description_
        transfer_no (_type_): _description_
        description (_type_): _description_
        amt (float, optional): _description_. Defaults to 0.0.
        deletion (bool, optional): _description_. Defaults to False.
        app (_type_, optional): _description_. Defaults to current_app.

    Returns:
        _type_: _description_
    """    

    # Find the account associated with the account sending money. 
    # Return false if not found.
    acc = Account.query.get(acc_no)
    if not acc:
        flash_codes(flash_code='0')
        return False
    
    if deletion:
        amt = acc.bal

    # Find the account associated with the account recieving money. 
    transfer_acc = Account.query.get(transfer_no)
    if not transfer_acc:
        flash_codes(flash_code='1')
        return False
    
    # Check that the account we want to transfer to is open.
    if not transfer_acc.status:
        flash_codes(flash_code='2')
        return False
    
    # Check that the usernames on both accounts match.
    if acc.username != transfer_acc.username:
        flash_codes(flash_code='3')
        return False

    # Get the current term.
    term = Curr_Term.query.all()[0].term

    # If we are deleting the account we skip this if, 
    # otherwise we need to do this.
    if not deletion:

        # Check if we are going to dip below the minimum balance allowed.
        if acc.bal - amt < acc.min_bal:
            flash_codes(flash_code='4')
            return False

    # Add transaction object for sending account.
    transaction_from = Transactions(acc_no=acc_no, amt=amt, 
                                    start_bal=acc.bal, 
                                    end_bal=acc.bal - amt, 
                                    withdrawal_deposit=False, 
                                    description=description, term=term)

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

    # Success code.
    flash_codes(flash_code='5')
    return True


def account_check(f):
    """A decorator to protect routes that access a specific account to ensure 
    that the account exists, is owned by the current user, and the account is 
    open.

    Args:
        f (function): The function that this is decorating.

    Returns:
        function/response: Returns the function in the case that the 
        tests are successful, if they are not the function redirects you.
    """    

    @wraps(f)
    def wrapper(acc_no, *args, **kwargs):
        # Get the account.
        acc = Account.query.get(acc_no)

        # Check the account exists.
        if not acc:
            flash_codes(flash_code='0', caller='account_check')
            return redirect(url_for('main.view_accounts'))
        
        # Check someone is logged in.
        if not current_user:
            flash_codes(flash_code='1', caller='account_check')
            return redirect(url_for('main.view_accounts'))

        # Check the current user owns this account.
        if acc.username != current_user.username:
            flash_codes(flash_code='2', caller='account_check')
            return redirect(url_for('main.view_accounts'))

        # Check that the account is open.
        if not acc.status:
            flash_codes(flash_code='3', caller='account_check')
            return redirect(url_for('main.view_accounts'))

        # Return the function result.
        return f(acc_no, *args, **kwargs)

    return wrapper


def account_exist(form, field):
    """A wtforms validator to check that the account exists.

    Args:
        form (FlaskForm): The flask form.
        field (IntegerField): The string field where the account number 
        is entered.

    Raises:
        ValidationError: An error is raised if account does not exist.
    """    

    # The account we need to get.
    acc = Account.query.get(int(field.data))

    # Check it exists.
    if not acc:
        raise ValidationError('That account does not exist.')
    

def account_history(acc_no):
    """Gather date data for transactions (x values), and balance data for 
    transactions (y values).

    Args:
        acc_no (int): The account number to get data for.

    Returns:
        tuple: A tuple of lists, the 0th index is labels and the 1st 
        index is values.
    """    

    # Get current balance.
    curr_bal = Account.query.get(acc_no).bal

    # Get all transactions for this account.
    transactions = Transactions.query.filter_by(acc_no=acc_no).all()
    
    sz = len(transactions)

    # Get starting point for data.
    labels = [format.format_date_2(datetime.now())]
    values = [curr_bal]


    # Iterate through transactions in reverse, doing this we can 
    # reconstruct prior balances so we can get data points.
    i = sz - 1
    while i >= 0:
        t = transactions[i]

        # If it is a withdrawal add to the current balance (going in reverse).
        if t.withdrawal_deposit == False:
            curr_bal += t.amt
        else:
            curr_bal -= t.amt

        # Add x and y to end of labels and values.
        dt = format.format_date_2(t.date)
        labels.append(dt)
        values.append(curr_bal)

        i -= 1

    # The data is currently in reverse order so reverse both lists.
    i = 0
    j = len(labels) - 1
    while i < j:
        labels[i], labels[j] = labels[j], labels[i]

        values[i], values[j] = values[j], values[i]

        i += 1
        j -= 1

    return labels, values
