from models import User, Account, Alerts, Messages, Bank_Settings, \
    Statements, Daily_Bal, Term_Data, Curr_Term, Transactions
from app import db
from datetime import datetime, date
from flask import Blueprint, render_template, redirect, flash, \
    request, current_app
from flask_login import login_required, current_user
from format import format_statement_filename, format_date_3, format_money
from pathlib import Path
from fpdf import Template
from pdf import PDF
from utils import check_access

class Admin_Tools():
    """
    Toolbox for admin users, these functions should 
    only be available to admins.
    """    

    def modify_bank_settings(savings_ir = -1.0, savings_min = -1.0, checkings_ir = -1.0, checkings_min = -1.0):
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
        if settings.savings_ir != -1.0:
            settings.savings_ir = savings_ir
        if settings.savings_min != -1.0:
            settings.savings_min = savings_min
        if settings.checkings_ir != -1.0:
            settings.checkings_ir = checkings_ir
        if settings.checkings_min != -1.0:
            settings.checkings_min = checkings_min

        # Commit To Database
        db.session.commit()

    def commit_all_compound():
        """
        Compounds the value on all accounts.
        """        
        accs = Account.query.all()

        # Add compound interest to account balance for each account.
        for acc in accs:
            acc.bal += acc.bal * acc.ir
        
        # Commit To Database
        db.session.commit()

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
        
        # Get Current Datetime
        dt = datetime.now()

        # Create New Message
        message = Messages(date=dt, username=username, content=content)

        # Add new message to database and commit.
        db.session.add(message)

        db.session.commit()

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

    def commit_daily_bal(acc_no, date=date.today()):
        # Get the account to commit account balance entry on.
        acc = Account.query.get(acc_no)

        # Create Daily_Bal object to store current balance.
        bal_statement = Daily_Bal(acc_no=acc_no, date=date, bal=acc.bal)

        # Add bal_statement to database and commit.
        db.session.add(bal_statement)

        db.session.commit()

    def commit_all_daily_bal():
        """
        Commit current balance to database.
        """        

        # Get all accounts
        accounts = Account.query.all()

        # Enter daily_bal into database.
        for account in accounts:
            Admin_Tools.commit_daily_bal(account.acc_no)

    def inc_term():
        """
        Increment current term to next term.
        """        

        term = Curr_Term.query.first()
        term.term += 1

        db.session.commit()

        accs = Account.query.all()

        for acc in accs:
            new_term = Term_Data(acc_no=acc.acc_no, term=term.term, start_bal=acc.bal)

            db.session.add(new_term)

            db.session.commit()

    def daily_processes():
        """
        These processes should be exexcuted daily.
        """

        Admin_Tools.commit_all_daily_bal()

    def term_processes():
        """
        These processes will be executed each term. Term starts sunday, 1 week long.
        """        

        Admin_Tools.commit_all_compound()
        Admin_Tools.assemble_all_statements()
        Admin_Tools.inc_term()

class Account_Metrics():
    """
    This class is used as a member of statement data it holds 
    all data related to an account.
    """    

    def __init__(self, account, term):
        """Initiate the account metrics object.

        Args:
            account (Account): Current Term
            term (int): The current term.
        """        
        
        # Get Total Balance for all accounts.
        self.acc_no = account.acc_no

        self.term = term

        self.start_bal = format_money(
            Term_Data.query.filter_by(acc_no=self.acc_no, 
                                      term=term).first().start_bal)

        self.end_bal = format_money(account.bal)

        self.transactions = Transactions.query.filter_by(
            acc_no=self.acc_no).all()

        self.withdrawal_total = 0.0

        self.deposit_total = 0.0

        for transaction in self.transactions:
            if transaction.withdrawal_deposit:
                self.deposit_total += transaction.amt
            else:
                self.withdrawal_total += transaction.amt

        self.withdrawal_total = format_money(self.withdrawal_total)
        self.deposit_total = format_money(self.deposit_total)

class Statement_Data():
    """
    Statement data object, passed to PDF class to write the Statement pdf.
    """    

    def __init__(self, username):
        """
        Initialize object and gather information, including 
        Account_Metrics object.

        Args:
            username (str): The username to gather data on.
        """        

        # Store username
        self.username = username

        # Store name of user.
        self.name = User.query.filter_by(username=username).first().name

        self.term = Curr_Term.query.all()[0].term

        # Get all accounts associated with user.
        self.accounts = Account.query.filter_by(username=username).all()

        self.savings_total = 0.0
        self.checkings_total = 0.0

        # Get account metrics object for each account.
        self.acc_metrics = {}
        for acc in self.accounts:
            if acc.acc_type == 0:
                self.savings_total += acc.bal
            elif acc.acc_type == 1:
                self.checkings_total += acc.bal

            self.acc_metrics[acc.acc_no] = Account_Metrics(acc, self.term)

        self.savings_total = format_money(self.savings_total)

        self.checkings_total = format_money(self.checkings_total)

        self.date = format_date_3(date.today())

    def get_acc_metrics(self):
        """
        Return the account metrics object.

        Returns:
            Account_Metrics: The account metrics object associated 
            with the username. 
        """     

        return self.acc_metrics

class Statement_Maker():
    """
    The statement maker class used to make statements for users. 
    """

    def __init__(self, username):
        """
        Initiate the Statement Maker Object for given username. 
        Prepares the pdf for writing.

        Args:
            username (str): The username to create a statement maker for.
        """        

        # Store username
        self.username = username

        self.state_data = Statement_Data(username=username)

        # Get the project root pth.
        self.project_root = current_app.config['PROJECT_ROOT']

        # Directory path to users pdf directory.
        dir_pth = self.project_root / Path('pdfs') / Path(self.username)

        # If directory path does not exist make the directory.
        if not dir_pth.exists():
            dir_pth.mkdir(parents=True)

        # The name of the file to write.
        name = format_statement_filename(self.username)

        # Get the full path of the file. PDF data is now ready to write.
        self.pth = dir_pth / Path(name)

        self.pdf = PDF(self.state_data, self.project_root)
        
        self.pdf.add_page()

        self.pdf.set_title('Statement For ' + self.state_data.date)

        self.pdf.set_author('henrymurdockbanking.me')

        self.pdf.overview()

        self.pdf.acc_summary()

        self.pdf.account_transactions()

    def write(self):
        """
        Outputs the pdf to the file path.
        """        
        # Write the pdf data.
        self.pdf.output(self.pth)

admin = Blueprint('admin', __name__)

@admin.route('/bank_settings/', methods=['POST', 'GET'])
@login_required
def bank_settings():
    if not check_access(current_user.id, 1):
        return redirect('profile.html')
    
    if request.method == 'POST':
        modifier = request.form['modifier']
        val = 0.0
        try:
            val = float(request.form['val'])

        except ValueError as err:
            flash('Invalid Value For Modifier')

        else:
            settings = Bank_Settings.query.get(1)

            if modifier == '0':
                settings.savings_ir = val
            elif modifier == '1':
                settings.savings_min = val
            elif modifier == '2':
                settings.checkings_ir = val
            elif modifier == '3':
                settings.checkings_min = val
            else:
                flash("Something Wrong!")

            db.session.commit()

    return render_template('bank_settings.html')

@admin.route('/send_alert/', methods=['POST', 'GET'])
@login_required
def send_alert():
    if not check_access(current_user.id, 1):
        return redirect('profile.html')
    
    if request.method == 'POST':
        content = request.form['content']

        if not content:
            flash('No Content Provided!')

        else:
            Admin_Tools.commit_alert(content=content)
    
    return render_template('send_alert.html')

@admin.route('/send_message/', methods=['POST', 'GET'])
@login_required
def send_message():
    if check_access(current_user.id, 1):
        return redirect('profile.html')
    
    if request.method == 'POST':
        username = request.form['username']
        content = request.form['content']

        if not content:
            flash('No Content Provided!')

        elif not username:
            flash('No Username Provided!')

        else:
            Admin_Tools.commit_message(content=content, username=username)

    return render_template('send_message.html')

@admin.route('/compound/', methods=['POST', 'GET'])
@login_required
def compound():
    if not check_access(current_user.id, 1):
        return redirect('profile.html')
    
    if request.method == 'POST':
        Admin_Tools.commit_compound()

    return render_template('compound.html')

@admin.route('/get_statements/', methods=['POST', 'GET'])
@login_required
def make_statements():
    if current_user.id != 1:
        flash('Only Admins Can Access That Page')
        return redirect('profile.html')
    
    if request.method == 'POST':
        Admin_Tools.assemble_all_statements()

    return render_template('make_statements.html')