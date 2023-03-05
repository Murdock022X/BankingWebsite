from flask import Blueprint, render_template, redirect, \
    request, flash, url_for, Response, send_file, current_app, \
        send_from_directory
from flask_login import login_required, current_user, LoginManager
from models import User, Account, Bank_Settings, Messages, \
    Alerts, Statements, Daily_Bal
from format import format_acc_no, format_money, format_acc, format_rates, \
    deep_format_acc, format_statement_filename, format_date, \
        format_date_for_graph
from werkzeug.security import check_password_hash
from app import db
from accounts import make_withdrawal, make_deposit, get_account, delete_acc, \
    checkings_savings_retrieval, get_accounts_user, transfer_all
from utils import get_messages, get_alerts, get_statements, get_statement
from pathlib import Path

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/profile/')
@login_required
def profile():
    user_accounts = Account.query.filter_by(username=current_user.username)

    user_accounts = [format_acc_no(acc.acc_no) for acc in user_accounts]
    return render_template('profile.html', user=current_user, 
                           accounts=user_accounts)

@main.route('/accounts/')
@login_required
def view_accounts():
    savings_accounts, checkings_accounts = \
                    checkings_savings_retrieval(current_user.username)

    return render_template('accounts.html', savings_accounts=savings_accounts,
                           checkings_accounts=checkings_accounts)

@main.route('/create_account/', methods=['POST', 'GET'])
@login_required
def create_account():
    rates = Bank_Settings.query.filter_by(id = 1).first()

    if request.method == 'POST':
        bal = 0.0
        min_bal = 0.0
        acc_type = 0
        ir = 0.0
        min_bal = 0.0

        try:
            bal = float(request.form['bal'])
            
        except ValueError as err:
            flash('Enter A Valid Balance')

        else:
            try:
                acc_type = int(request.form['acc_type'])

                if acc_type == 0:
                    ir = rates.savings_ir
                    min_bal = rates.savings_min
                
                else:
                    ir = rates.checkings_ir
                    min_bal = rates.checkings_min

            except ValueError as err:
                flash('Select A Valid Account Type')

            else:
                if bal < min_bal:
                    flash('Starting Balance Smaller Than Minimum Balance Allowed')
                
                else:
                    new_acc = Account(acc_type=acc_type, username=current_user.username, ir=ir, min_bal=min_bal, bal=bal)
                    db.session.add(new_acc)
                    db.session.commit()
                    return redirect(url_for('main.view_accounts'))
    
    format_rates(rates)
    return render_template('create_acc.html', rates=rates)

@main.route('/summary/')
@login_required
def summary():
    accs = get_accounts_user(username=current_user.username)
    user_accounts = []
    for acc in accs:
        user_accounts.append(deep_format_acc(acc))
        
    return render_template('summary.html', accounts=user_accounts)

@main.route('/<int:acc_no>/withdraw/', methods=['GET', 'POST'])
@login_required
def withdraw(acc_no):
    if request.method == 'POST':
        try:
            amt_withdraw = float(request.form['bal'])
        
        except ValueError as err:
            flash('Please Provide A Valid Amount To Withdraw')

        else:
            make_withdrawal(acc_no, amt_withdraw)

            return redirect(url_for('main.view_accounts'))

    return render_template('withdraw.html')

@main.route('/<int:acc_no>/deposit/', methods=['GET', 'POST'])
@login_required
def deposit(acc_no):
    if request.method == 'POST':
        try:
            amt_deposit = float(request.form['bal'])
        
        except ValueError as err:
            flash('Please Provide A Valid Amount To Deposit')

        else:
            make_deposit(acc_no, amt_deposit)

            return redirect(url_for('main.view_accounts'))

    return render_template('deposit.html')

@main.route('/<int:acc_no>/delete_account/', methods=['GET', 'POST'])
@login_required
def delete_account(acc_no):
    if request.method == 'POST':
        transfer_no = 0

        try:
            transfer_no = int(request.form['acc_no'])

        except ValueError as err:
            flash('Invalid Account Transfer Number')

        else:
            password = request.form['password']

            hash = current_user.password

            if check_password_hash(hash, password):
                transfer_status = transfer_all(acc_no, transfer_no)

                if not transfer_status:
                    flash('Invalid Account Transfer Number')
                
                else:
                    delete_acc(acc_no)

                    return redirect(url_for('main.view_accounts'))


            else:
                flash('Incorrect Password')

    return render_template('delete.html', account_number=format_acc_no(acc_no))

@main.route('/<int:acc_no>/account_info/')
@login_required
def account_info(acc_no):
    acc = deep_format_acc(get_account(acc_no))
    return render_template('account_info.html', acc=acc)

@main.route('/alerts/')
@login_required
def alerts():
    alerts = get_alerts()

    return render_template('alerts.html', alerts=alerts)

@main.route('/messages/')
@login_required
def messages():
    messages = get_messages(current_user.username)

    return render_template('messages.html', messages=messages)

@main.route('/<int:id>/delete_messages/')
@login_required
def delete_message(id):
    message = Messages.query.get(id)

    db.session.delete(message)

    db.session.commit()

    return redirect(url_for('main.messages'))

@main.route('/view_eStatements/', methods=['GET','POST'])
@login_required
def view_eStatements():
    statements = Statements.query.filter_by(username=current_user.username)

    filenames = {}

    for statement in statements:
        filenames[statement.id] = Path(statement.path).parts[-1]

    return render_template('eStatements.html', statements=statements, filenames=filenames)

@main.route('/<int:id>/get_eStatement/', methods=['GET','POST'])
@login_required
def get_eStatement(id):
    statement = Statements.query.get(id)

    pdf_pth = statement.path

    pp = Path(pdf_pth)
    
    file_name = pp.parts[-1]

    return send_file(pdf_pth, as_attachment=True)

@main.route('/<int:acc_no>/account_graph/')
@login_required
def account_graph(acc_no):
    data = Daily_Bal.query.filter_by(acc_no=acc_no)

    valid = False
    
    sz = 0
    for acc in data:
        sz += 1
        if sz > 1:
            valid = True
            break
        

    url = url_for("main.account_graph_data", acc_no=acc_no)

    return render_template('account_graph.html', acc_no=acc_no, url=url, valid=valid)

@main.route('/<int:acc_no>/account_graph_data/')
@login_required
def account_graph_data(acc_no):
    monthly_balances = Daily_Bal.query.filter_by(acc_no=acc_no)

    labels = [format_date_for_graph(month.date) for month in monthly_balances]
    values = [month.bal for month in monthly_balances]

    chart_max = max(values) * 1.25
    step_val = max(values) * 1.25 / 20

    return {"labels": labels, "values": values, "chart_max": chart_max, "step_val": step_val}