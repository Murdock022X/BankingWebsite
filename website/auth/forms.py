from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length

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