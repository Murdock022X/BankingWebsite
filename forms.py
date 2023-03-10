from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, DecimalField, \
    SelectField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length
from models import User

def IsUser(username):
    if not User.query.filter_by(username=username):
        return False
    
    return True

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), 
                                                   Length(min=6, max=100)])

    password = PasswordField('Password', validators=[DataRequired(), 
                                                   Length(min=6, max=100)])

    name = StringField('Name', validators=[DataRequired(), Length(max=1000)])

    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), 
                                                   Length(min=6, max=100)])

    password = PasswordField('Password', validators=[DataRequired(), 
                                                   Length(min=6, max=100)])
    
    submit = SubmitField('Login')

class CreateAccountForm(FlaskForm):
    acc_type = SelectField('Account Type', 
                            choices=[(0, 'Savings'), (1, 'Checkings')], 
                            validators=[DataRequired()])
    
    balance = DecimalField('Balance', validators=[DataRequired()])

    password = PasswordField('Password', validators=[DataRequired(), 
                                                   Length(min=6, max=100)])
    
    submit = SubmitField('Create Account')

class WithdrawalForm(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])

    amt = DecimalField('Amount', validators=[DataRequired()])

    submit = SubmitField('Withdraw')

class DepositForm(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])

    amt = DecimalField('Amount', validators=[DataRequired()])

    submit = SubmitField('Deposit')

class DeleteAccountForm(FlaskForm):
    transfer_no = IntegerField('Transfer Number')

    password = PasswordField('Password', validators=[DataRequired(), 
                                                   Length(min=6, max=100)])
    
    submit = SubmitField('Delete')

class BankSettingsForm(FlaskForm):
    change_type = SelectField('Change Type', 
                              choices=[(0, 'Savings APY'), 
                                       (1, 'Checkings APY'), 
                                       (2, 'Savings Minimum Balance'), 
                                       (3, 'Checkings Minimum Balance')],
                              validators=[DataRequired()])
    
    new_value = DecimalField('New Value', validators=[DataRequired()])

    submit = SubmitField('Commit Change')

class SendAlertForm(FlaskForm):
    content = TextAreaField('Content',
                            validators=[DataRequired()])
    
    submit = SubmitField('Send Alert')
    
class SendMessageForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), 
                                                   Length(min=6, max=100)])

    content = TextAreaField('Content', validators=[DataRequired()])

    submit = SubmitField('Send Message')
