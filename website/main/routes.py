from flask import Blueprint, render_template, redirect, url_for, send_file

from flask_login import login_required, current_user

from website.models import Account, Bank_Settings, Messages, Statements, \
    Transactions, db

from website.utils.format import format_acc_no, format_rates, \
    deep_format_acc, format_date_3

from werkzeug.security import check_password_hash

from website.main.utils import make_withdrawal, make_deposit, \
    checkings_savings_retrieval, get_accounts_user, transfer, create_acc, \
    Account_History

from website.utils.utils import get_messages, get_alerts

from pathlib import Path

from website.main.forms import WithdrawalForm, DepositForm, \
    CreateAccountForm, CloseAccountForm

from website.utils.flash_codes import flash_codes

# Create the main blueprint route
main = Blueprint('main', __name__)

@main.route('/')
def home():
    """Renders the html for the home page.

    Returns:
        str: The rendered html page with values filled in.
    """    
    return render_template('home.html')


@main.route('/profile/')
@login_required
def profile():
    """Collects accounts associated with the logged in user 
    and renders the profile template with those values.

    Returns:
        str: The rendered html page.
    """    

    # Collect accounts associated with this user.
    user_accounts = Account.query.filter_by(username=current_user.username)

    user_accounts = [deep_format_acc(acc) for acc in user_accounts]

    print(user_accounts)

    # Passes relevant data to the template and renders.
    return render_template('profile.html', user=current_user, 
                           accounts=user_accounts)


@main.route('/accounts/')
@login_required
def view_accounts():
    """Renders the template for the view accounts page, retrieves all 
    checkings and savings accounts seperated by account type (see 
    checkings_savings_retrieval) and passes to render template function.

    Returns:
        str: The rendered html page.
    """    

    # Retrieves checkings and savings information.
    savings_accounts, checkings_accounts = \
                    checkings_savings_retrieval(current_user.username)

    # Passes off info to render template to view accounts.
    return render_template('accounts.html', savings_accounts=savings_accounts,
                           checkings_accounts=checkings_accounts)


@main.route('/create_account/', methods=['POST', 'GET'])
@login_required
def create_account():
    """Renders the template used to create accounts and also takes input from 
    the form to create accounts when submitted.

    Returns:
        str/response: Returns the rendered html string in the case of a get 
        request or in the case of a post request where account creation fails. 
        Returns a redirect response in the case of successful post request 
        account creation.
    """    

    flash_offset = 0

    # Get the rates to display for both account types.
    rates = Bank_Settings.query.get(1)
    
    # Create the create account form.
    form = CreateAccountForm()

    # If form is validated and submitted.
    if form.validate_on_submit():
        # Get the min_bal and apy based on account type.
        min_bal = rates.savings_min
        apy = rates.savings_apy

        if form.acc_type.data == 1:
            min_bal = rates.checkings_min
            apy = rates.checkings_apy

        # Flash a message if the requested starting bal is smaller 
        # than the min bal allowed on the account.
        if form.balance.data < min_bal:
            flash_codes(flash_code='0', flash_offset=flash_offset)

        # Ready for account creation.
        else:
            # Create account.
            create_acc(username=current_user.username, bal=form.balance.data, 
                       min_bal=min_bal, apy=apy, acc_type=form.acc_type.data)

            # Flash account creation message.
            flash_codes(flash_code='1', flash_offset=flash_offset)

            # Return redirection response to view accounts endpoint.
            return redirect(url_for('main.view_accounts'))
    
    # Format rates for html page.
    rates = format_rates(rates)

    # Renders the template with relevant data.
    return render_template('create_acc.html', rates=rates, form=form)


@main.route('/summary/')
@login_required
def summary():
    """The account summary page, which displays a simple breakdown of accounts.

    Returns:
        str: Rendered html string.
    """    

    # Get accounts for this user.
    accs = get_accounts_user(username=current_user.username)

    # Create a list of dictionaries with formatted data for each account 
    # attribute.
    user_accounts = []
    for acc in accs:
        user_accounts.append(deep_format_acc(acc))
        
    # Renders the html string with data.
    return render_template('summary.html', accounts=user_accounts)


@main.route('/<int:acc_no>/withdraw/', methods=['GET', 'POST'])
@login_required
def withdraw(acc_no):
    """A page with a form to withdraw money from the selected account.

    Args:
        acc_no (int): The account number we should withdraw from.

    Returns:
        str/response: Returns an html string in the case of a get request or 
        a post request that isn't successful at withdrawing. In the case of 
        a successful post request a redirect response is sent.
    """    

    flash_offset = 2

    # Create the account withdrawal form.
    form = WithdrawalForm()

    # Checks if the form has been validated and submitted.
    if form.validate_on_submit():

        # Use make_withdrawal function to make a withdrawal from the account.
        flash_code = make_withdrawal(acc_no=acc_no, amt=form.amt.data, 
                                     description=form.description.data)
        
        # Withdrawal failed.
        if flash_code == '0' or flash_code == '1':
            flash_codes(flash_code=flash_code, flash_offset=flash_offset)

        # Return the redirect response to view accounts.
        else:
            flash_codes(flash_code=flash_code, flash_offset=flash_offset)
            return redirect(url_for('main.view_accounts'))

    return render_template('withdraw.html', form=form)


@main.route('/<int:acc_no>/deposit/', methods=['GET', 'POST'])
@login_required
def deposit(acc_no):
    """A page with a form to deposit money into the selected account.

    Args:
        acc_no (int): The account number we should deposit to.

    Returns:
        str/response: Returns an html string in the case of a get request or 
        a post request that isn't successful at depositing. In the case of 
        a successful post request a redirect response is sent.
    """   

    flash_offset = 5

    # Create the deposit form. 
    form = DepositForm()

    # Check if the form has been validated and submitted.
    if form.validate_on_submit():

        # Make a deposit into the account.
        flash_code = make_deposit(acc_no=acc_no, amt=form.amt.data, 
                                        description=form.description.data)

        if flash_code == '0':
            flash_codes(flash_code=flash_code, flash_offset=flash_offset)

        else:
            flash_codes(flash_code=flash_code, flash_offset=flash_offset)
            
            # Return a redirect response to the view accounts page.
            return redirect(url_for('main.view_accounts'))

    # Return a rendered html string.
    return render_template('deposit.html', form=form)


@main.route('/<int:acc_no>/close_account/', methods=['GET', 'POST'])
@login_required
def close_account(acc_no):
    """Delete the selected account, also has an option to transfer the balance on this account to another account.

    Args:
        acc_no (int): The account number we should delete.

    Returns:
        str/response: Returns an html string in the case of a get request or 
        a post request that isn't successful at deleting. In the case of 
        a successful post request a redirect response is sent.
    """    

    flash_offset = 7

    # Create the delete account form.
    form = CloseAccountForm()

    # Check if the form has been validated and submitted.
    if form.validate_on_submit():

        # Get the stored password hash.
        hash = current_user.password

        # Check the entered password against the password hash.
        if check_password_hash(hash, form.password.data):
            transfer_code = '4'

            if form.transfer_no.data:
                # Transfer all money to a different account.
                transfer_code = transfer(acc_no, form.transfer_no.data, 
                                            description='Upon deletion of'
                                                ' account ' + \
                                                    format_acc_no(acc_no) + \
                                                        ', funds transferred to'
                                                        ' this account.', 
                                                        deletion=True)

                # Increment flash offset by one because first error code
                # for the function is password error.
                flash_codes(flash_code=transfer_code, flash_offset=flash_offset + 1)
            
            if transfer_code == '4':
                acc = Account.query.get(acc_no)
                acc.close()   

                # Commit our changes made in functions.
                db.session.commit()

                # Success.
                flash_codes(flash_code='5', flash_offset=flash_offset)

                # Return redirect response to view accounts.
                return redirect(url_for('main.view_accounts'))

        else:
            flash_codes(flash_code='0', flash_offset=flash_offset)

    # Return the rendered html string with the data inserted.
    return render_template('delete.html', account_number=format_acc_no(acc_no), form=form)


# Route removed as it was unhelpful.
# @main.route('/<int:acc_no>/account_info/')
# @login_required
# def account_info(acc_no):
#     """A page that displays information for just one account.
#
#     Args:
#         acc_no (int): The account number.
#
#     Returns:
#         str: The rendered html string.
#     """    
#
#     acc = deep_format_acc(get_account(acc_no))
#     return render_template('account_info.html', acc=acc)


@main.route('/alerts/')
@login_required
def alerts():
    """Displays all alerts issued.

    Returns:
        str: The rendered html string displaying alerts.
    """    

    # Get all the alert objects.
    alerts = get_alerts()

    # Render the html string.
    return render_template('alerts.html', alerts=alerts)


@main.route('/messages/')
@login_required
def messages():
    """Displays all messages issued.

    Returns:
        str: The rendered html string displaying messages.
    """    

    # Get all message objects for the current user.
    messages = get_messages(current_user.username)

    # Return the rendered html string.
    return render_template('messages.html', messages=messages)


@main.route('/<int:id>/delete_messages/')
@login_required
def delete_message(id):
    """Delete the selected account.

    Args:
        id (int): The id of the message to delete.

    Returns:
        response: The redirect response which redirects back to messages route.
    """    

    # Get the message object associated with this id.
    message = Messages.query.get(id)

    # Delete the object.
    db.session.delete(message)

    # Commit to database.
    db.session.commit()

    # Redirect to messages view.
    return redirect(url_for('main.messages'))


@main.route('/view_eStatements/', methods=['GET','POST'])
@login_required
def view_eStatements():
    """A page where you can download all E-Statements 
    associated with this user account.

    Returns:
        str: The rendered html string page with a link to download 
        each statement.
    """    

    # Get the statements associated with this user.
    statements = Statements.query.filter_by(username=current_user.username)

    # Get filenames and dates.
    filenames = {}
    dates = {}

    # Populate with statement id routing to filename and dates.
    for statement in statements:
        filenames[statement.id] = Path(statement.path).parts[-1]
        dates[statement.id] = format_date_3(statement.date)

    # Returb the rendered html string.
    return render_template('eStatements.html', statements=statements, 
                           filenames=filenames, dates=dates)


@main.route('/<int:id>/get_eStatement/', methods=['GET','POST'])
@login_required
def get_eStatement(id):
    """Send the file to the user for the requested statement.

    Args:
        id (int): The id for the e-statement requested.

    Returns:
        response: The pdf file.
    """    

    # Get the statement associated with the id.
    statement = Statements.query.get(id)

    # Get the path to the pdf.
    pdf_pth = statement.path

    # Return the pdf response as a downloadable attachment.
    return send_file(pdf_pth, as_attachment=True)


@main.route('/<int:acc_no>/account_graph/')
@login_required
def account_graph(acc_no):
    """Display a graph of account history for the selected account.

    Args:
        acc_no (int): The selected account.

    Returns:
        str: The rendered html string.
    """    

    # The balance data.
    data = Transactions.query.filter_by(acc_no=acc_no).all()


    valid = False
    
    # If we have more than 1 data point we can display the graph at this 
    # point so we set valid to true. 
    if len(data) >= 1:
        valid = True
        
    # Pass this url to the html page so it can be given to javascript, 
    # this was javascript can access the account_graph_data endpoint.
    url = url_for("main.account_graph_data", acc_no=acc_no)

    # Return the rendered html string.
    return render_template('account_graph.html', acc_no=acc_no, url=url, 
                           valid=valid)


@main.route('/<int:acc_no>/account_graph_data/')
@login_required
def account_graph_data(acc_no):
    """An endpoint to be used by javascript to retrieve balance data 
    associated with the account. Data is serialized into json format.

    Args:
        acc_no (int): The account number to retrieve balance data for.

    Returns:
        dict: A dictionary mapping "labels" to x values and "values" 
        to y values.
    """    

    # Retrieve balance data.
    acc_hist = Account_History(acc_no)

    # Return with "labels" and "values".
    return {"labels": acc_hist.labels, "values": acc_hist.values}