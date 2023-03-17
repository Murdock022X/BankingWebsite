from flask_wtf import FlaskForm
from wtforms import SelectField, DecimalField, SubmitField, StringField, \
    IntegerField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, InputRequired, Length, Optional
from website.main.utils import account_exist

class CreateAccountForm(FlaskForm):
    acc_type = SelectField('Account Type', 
                            choices=[(0, 'Savings'), (1, 'Checkings')], 
                            validators=[DataRequired()])
    
    balance = DecimalField('Balance', validators=[InputRequired()])
    
    submit = SubmitField('Create Account')

class WithdrawalForm(FlaskForm):
    description = TextAreaField('Description', validators=[DataRequired()])

    amt = DecimalField('Amount', validators=[InputRequired()])

    submit = SubmitField('Withdraw')

class DepositForm(FlaskForm):
    description = TextAreaField('Description', validators=[DataRequired()])

    amt = DecimalField('Amount', validators=[InputRequired()])

    submit = SubmitField('Deposit')

class CloseAccountForm(FlaskForm):
    transfer_no = IntegerField('Transfer Number', validators=[Optional(), account_exist])

    password = PasswordField('Password', validators=[DataRequired(), 
                                                   Length(min=6, max=100)])
    
    submit = SubmitField('Close Account')

class TransferForm(FlaskForm):
    transfer_no = IntegerField('Transfer Number', validators=[InputRequired(), account_exist])
    
    amt = DecimalField('Amount To Transfer', validators=[InputRequired()])

    description = TextAreaField('Note On Transfer', validators=[Optional()])

    submit = SubmitField('Transfer')