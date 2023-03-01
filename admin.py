from models import User, Account, Alerts, Messages, Bank_Settings, Statements
from app import db
from datetime import datetime, date
from flask import Blueprint, render_template, redirect, flash, request, current_app
from flask_login import login_required, current_user
from utils import MyFPDF
from format import format_statement_filename
from pathlib import Path

class Admin_Tools():

    def modify_bank_settings(savings_ir = -1.0, savings_min = -1.0, checkings_ir = -1.0, checkings_min = -1.0):
        settings = Bank_Settings.query.get(1)

        if settings.savings_ir != -1.0:
            settings.savings_ir = savings_ir
        if settings.savings_min != -1.0:
            settings.savings_min = savings_min
        if settings.checkings_ir != -1.0:
            settings.checkings_ir = checkings_ir
        if settings.checkings_min != -1.0:
            settings.checkings_min = checkings_min

        db.session.commit()

        return True

    def commit_compound():
        accs = Account.query.all()

        for acc in accs:
            acc.bal *= acc.ir
        
        db.session.commit()

        return True

    def commit_alert(content):
        dt = datetime.now()
        
        alert = Alerts(date=dt, content=content)

        db.session.add(alert)

        db.session.commit()

        return True
    
    def commit_message(self, content, username):
        dt = datetime.now()

        message = Messages(date=dt, username=username, content=content)

        db.session.add(message)

        db.session.commit()

        return True

    def assemble_statements():
        users = User.query.all()

        for user in users:
            sm = Statement_Maker(user.username)

            statement = Statements(username=user.username, date=date.today(), name=sm.state_data.name, path=str(sm.pth))
            db.session.add(statement)

            db.session.commit()

            sm.write()


class Account_Metrics():

    def __init__(self, accounts):
        
        self.total_bal = 0

        for acc in accounts:
            self.total_bal += acc.bal

class Statement_Maker(Admin_Tools):
    def __init__(self, username):
        self.username = username
        self.state_data = Statement_Data(username)
        self.pdf = MyFPDF()
        self.pdf.add_page()
        html_page = render_template('eStatement_form.html', statement_data=self.state_data)
        self.pdf.write_html(html_page) 

        project_root = current_app.config['PROJECT_ROOT']
        dir_pth = project_root / Path('pdfs') / Path(self.username)
        if not dir_pth.exists():
            dir_pth.mkdir(parents=True)

        name = format_statement_filename(self.username)

        self.pth = dir_pth / Path(name)

    def write(self):
        self.pdf.output(name=self.pth)

class Statement_Data():

    def __init__(self, username):
        self.username = username

        self.name = User.query.filter_by(username=username).first().name

        accounts = Account.query.filter_by(username=username)
        self.acc_metrics = Account_Metrics(accounts=accounts)

    def get_acc_metrics(self):
        return self.acc_metrics

admin = Blueprint('admin', __name__)

@admin.route('/bank_settings/', methods=['POST', 'GET'])
@login_required
def bank_settings():
    if current_user.id != 1:
        flash('Only Admins Can Access That Page')
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
    if current_user.id != 1:
        flash('Only Admins Can Access That Page')
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
    if current_user.id != 1:
        flash('Only Admins Can Access That Page')
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
    if current_user.id != 1:
        flash('Only Admins Can Access That Page')
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
        Admin_Tools.assemble_statements()

    return render_template('make_statements.html')