from website.models import User, Account, Alerts, Messages, Bank_Settings, \
    Statements, Term_Data, Curr_Term, Transactions
from datetime import datetime, date
from website.admin.pdf import Statement_Maker
from website import db
from website.utils.utils import term_interest
from wtforms.validators import ValidationError
from website.utils.flash_codes import flash_codes
from functools import wraps
from flask import redirect, url_for
from flask_login import current_user

def admin_only(f):
    """Check that the user accessing a route is an admin.

    Args:
        f (function): The function we are trying to access.

    Returns:
        function/response: In the case of a successful check we call 
        the function with the parameters, thus wrapping it. In the case 
        of a failure we return a redirect to main.profile.
    """    

    # This function wraps another function.
    @wraps(f)
    def wrapper(*args, **kwargs):

        # If the current user id is not 1 then user is not admin.
        if current_user.id != 1:

            # Flash code and redirect.
            flash_codes(caller='admin_only')
            return redirect(url_for('main.profile'))
        
        # Return the function call.
        return f(*args, **kwargs)
    
    return wrapper

def user_exists(form, field):
    """Validator for wtforms. Ensures that for a given username, 
    a user exists for that username.

    Args:
        form (FlaskForm): The given form.
        field (wtforms.StringField): A string field from wtforms 
        that has been filled out by user.

    Raises:
        ValidationError: Raises an error that the field is not valid if we 
        cannot find a user in the database related to this user.
    """    

    if not User.query.filter_by(username=field.data).first():
        raise ValidationError('This user does not exist.')
    

class Admin_Tools():
    """
    Toolbox for admin users, these functions should 
    only be available to admins.
    """    

    def modify_bank_settings(new_value, change_type):
        """Changes necessary bank setting to new setting.

        Args:
            savings_ir (float, optional): Savings interest rate. Defaults to -1.0.
            savings_min (float, optional): Savings minimum balance. Defaults to -1.0.
            checkings_ir (float, optional): Checkings interest rate. Defaults to -1.0.
            checkings_min (float, optional): Checkings minimum balance. Defaults to -1.0.
        """
        

        # Retrieve current settings
        settings = Bank_Settings.query.get(1)

        # Update the correct interest rate or minimum balance allowed.
        

        # Commit To Database
        db.session.commit()


    def compound_acc(acc):
        """Compound the balance on an account, this should be 
        activated at end of term. Also stores the transaction.

        Args:
            acc (Account): The account to modify with new balances.
        """        

        # Get the current term.
        term = Curr_Term.query.first().term

        # Get the interest rate for the term. Term = 1 week, to keep things 
        # simple we assume exactly 52 weeks in the year, i.e don't account 
        # for leap years, or extra days in the 52nd week.
        dividends = acc.bal * term_interest(acc.apy)

        # Create the account transaction.
        transaction = Transactions(acc_no=acc.acc_no, term=term, 
                                   start_bal=acc.bal, 
                                   end_bal=acc.bal + dividends, 
                                   date=datetime.now(), amt=dividends, 
                                   withdrawal_deposit=True, 
                                   description='Dividend deposit.')

        # Add the calculated dividends to the balance.
        acc.bal += dividends
        
        # Add the transaction to session.
        db.session.add(transaction)

        # Commit.
        db.session.commit()


    def commit_all_compound():
        """
        Compounds the value on all accounts. Activate at end of term.
        """    

        # Get all the accounts.    
        accs = Account.query.all()

        # Add compound interest to account balance for each account.
        for acc in accs:
            if acc.status:
                Admin_Tools.compound_acc(acc)


    def commit_alert(content):
        """
        Commits an alert to the database. (Messages are sent to specific 
        users, alerts are sent to all users.)

        Args:
            content (str): The content to send in the alert.
        """        

        # Get Current Datetime
        dt = datetime.now()
        
        # Create New Alert
        alert = Alerts(date=dt, content=content)

        # Add new alert to database and commit.
        db.session.add(alert)

        db.session.commit()
    

    def commit_message(content, username):
        """Commit a message to the database. (Messages are sent to specific 
        users, alerts are sent to all users.)

        Args:
            content (str): The message content.
            username (str): The username for the user to send to.
        """        
        
        user = User.query.filter_by(username=username).first()

        if not user:
            return '0'

        # Get Current Datetime
        dt = datetime.now()

        # Create New Message
        message = Messages(date=dt, username=username, content=content)

        # Add new message to database and commit.
        db.session.add(message)

        db.session.commit()

        return '1'
    

    def assemble_all_statements():
        """
        Assemble statements for all users.
        """        

        # Get all users
        users = User.query.all()

        # For each user write a statement and send to database.
        for user in users:
            # Initiate a Statement_Maker object for the current user.
            sm = Statement_Maker(user.username)

            # Create an entry in the Statements database with the path to the pdf.
            check_statement = Statements.query.filter_by(username=user.username, date=date.today()).first()

            if not check_statement:
                statement = Statements(username=user.username, date=date.today(), name=sm.state_data.name, path=str(sm.pth))
            
                # Add Statement entry to database and commit.
                db.session.add(statement)

                db.session.commit()

            # Write the pdf to the filepath.
            sm.write()


#
# Function no longer in use.
#     def commit_bal_data(acc_no, date=date.today()):
#         """Commit data on the current balance of this account to database.
#
#         Args:
#             acc_no (int): The account number to commit balance data for.
#             date (date, optional): A date object to store the time for which 
#             this balance was taken. Defaults to date.today().
#         """        
# 
#         # Get the account to commit account balance entry on.
#         acc = Account.query.get(acc_no)
#
#         # Create Daily_Bal object to store current balance.
#         bal_statement = Balance_Data(acc_no=acc_no, date=date, bal=acc.bal)
# 
#         # Add bal_statement to database and commit.
#         db.session.add(bal_statement)
#
#         db.session.commit()


#
# This function is no longer useful.
#     def commit_all_bal_data():
#         """
#         Commit current balance to database.
#         """        
#
#         # Get all accounts
#         accounts = Account.query.all()
# 
#         # Enter daily_bal into database.
#         for account in accounts:
#             Admin_Tools.commit_bal_data(account.acc_no)


    def inc_term():
        """
        Increment current term to next term.
        """        

        # Get the current term and increment.
        term = Curr_Term.query.first()
        term.term += 1

        db.session.commit()

        # Get all accounts
        accs = Account.query.all()

        # Create a new term data entry for all acounts.
        for acc in accs:

            # Create the term data object.
            new_term = Term_Data(acc_no=acc.acc_no, term=term.term, 
                                 start_bal=acc.bal)

            # Add the term data object to session and commit.
            db.session.add(new_term)

            db.session.commit()

#
# Function no longer useful.
#
#     def daily_processes():
#         """
#         These processes should be exexcuted daily.
#         """
#
#         # Commit balances for all accounts.
#         Admin_Tools.commit_all_bal_data()


    def term_processes():
        """
        These processes will be executed each term. Term starts sunday, 1 week long.
        """        

        # Compound all accounts at the end of term.
        Admin_Tools.commit_all_compound()

        # Assemble statements for all users.
        Admin_Tools.assemble_all_statements()

        # Increment the current term.
        Admin_Tools.inc_term()