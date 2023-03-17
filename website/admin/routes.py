from website.models import Bank_Settings, db
from flask import Blueprint, render_template
from flask_login import login_required
from website.utils.format import format_rates
from website.admin.forms import BankSettingsForm, SendAlertForm, SendMessageForm
from website.utils.flash_codes import flash_codes
from website.admin.utils import Admin_Tools, admin_only

# Create the admin blueprint to be used for privelged actions.
admin = Blueprint('admin', __name__)


@admin.route('/bank_settings/', methods=['POST', 'GET'])
@login_required
@admin_only
def bank_settings():
    """Route for bank settings page allows admin to alter bank rates.

    Returns:
        str: Render the page for 'bank_settings.html', takes the form.
    """   

    # Create the form.
    form = BankSettingsForm()
    old_rates = Bank_Settings.query.get(1)

    # Form submission.
    if form.validate_on_submit():
        change_type = int(form.change_type.data)

        # Adjust rates appropriately.
        if change_type == 0:
            old_rates.savings_apy = form.new_value.data
        elif change_type == 1:
            old_rates.checkings_apy = form.new_value.data
        elif change_type == 2:
            old_rates.savings_min = form.new_value.data
        elif change_type == 3:
            old_rates.checkings_min = form.new_value.data

        db.session.commit()

        flash_codes()

    settings = format_rates(old_rates)
    return render_template('bank_settings.html', form=form, rates=settings)


@admin.route('/send_alert/', methods=['POST', 'GET'])
@login_required
@admin_only
def send_alert():
    """A admin only route to send alerts with. Can only be accessed by admin.

    Returns:
        str: The rendered html page.
    """    

    # Create a send alert form.
    form = SendAlertForm()

    # On form validation and submission.
    if form.validate_on_submit():
        Admin_Tools.commit_alert(content=form.content.data)
        flash_codes()
    
    return render_template('send_alert.html', form=form)


@admin.route('/send_message/', methods=['POST', 'GET'])
@login_required
@admin_only
def send_message():    
    """Allows an admin to send a message to a user in the database.

    Returns:
        str: The rendered html string.
    """    

    # Fields are string for username, textarea field for content, and a 
    # submit field.
    form = SendMessageForm()

    # On form validation and submission, checks 
    # that username provided belongs to a user.
    if form.validate_on_submit():
        flash_code = Admin_Tools.commit_message(content=form.content.data, 
                                                username=form.username.data)
        flash_codes(flash_code=flash_code)

    return render_template('send_message.html', form=form)

# @admin.route('/compound/', methods=['POST', 'GET'])
# @login_required
# def compound():
#     if not check_access(current_user.id, 1):
#         return redirect('profile.html')
#    
#     if request.method == 'POST':
#         Admin_Tools.commit_compound()
# 
#     return render_template('compound.html')

# @admin.route('/get_statements/', methods=['POST', 'GET'])
# @login_required
# def make_statements():
#     if current_user.id != 1:
#         flash('Only Admins Can Access That Page')
#         return redirect('profile.html')
#     
#     if request.method == 'POST':
#         Admin_Tools.assemble_all_statements()
# 
#     return render_template('make_statements.html')