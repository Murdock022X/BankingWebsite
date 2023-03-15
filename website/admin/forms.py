from flask_wtf import FlaskForm
from wtforms import SelectField, DecimalField, SubmitField, StringField, \
    TextAreaField
from wtforms.validators import DataRequired, InputRequired, Length
from website.admin.utils import user_exists

class BankSettingsForm(FlaskForm):
    change_type = SelectField('Change Type', 
                              choices=[(0, 'Savings APY'), 
                                       (1, 'Checkings APY'), 
                                       (2, 'Savings Minimum Balance'), 
                                       (3, 'Checkings Minimum Balance')],
                              validators=[DataRequired()])
    
    new_value = DecimalField('New Value', validators=[InputRequired()])

    submit = SubmitField('Commit Change')

class SendAlertForm(FlaskForm):
    content = TextAreaField('Content',
                            validators=[DataRequired()])
    
    submit = SubmitField('Send Alert')
    
class SendMessageForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), 
                                                   Length(min=6, max=100),
                                                   user_exists])

    content = TextAreaField('Content', validators=[DataRequired()])

    submit = SubmitField('Send Message')