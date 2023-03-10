from flask import Blueprint, render_template, redirect, request, url_for, \
    flash, current_app
from flask_login import LoginManager, login_user, logout_user, current_user, \
    login_required
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from app import db
from admin import Admin_Tools
import logger
from datetime import datetime
from forms import SignupForm, LoginForm

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        # Find user with username data
        user = User.query.filter_by(username=form.username.data).first()
        # Check if there is a user with that username if so check password

        if user:
            
            # Get the password hash
            hash = user.password

            # Check the password against hash
            if check_password_hash(hash, form.password.data):
                login_user(user)

                logger.Logger.log_general('Logged In:', form.username.data)

                # Redirect to profile
                return redirect(url_for('main.profile'))
            
            else:
                flash('Incorrect Password')

        else:
            flash('User Not Found')

    return render_template('login.html', form=form)

@auth.route('/signup/', methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        # Query for other users
        check_users = User.query.filter_by(username=form.username.data).first()

        # Good to continue if no other users with this username
        if not check_users:
            # Generate password hash and create new User entry
            hash = generate_password_hash(form.password.data, method='sha256')
            new_user = User(username=form.username.data, name=form.name.data, password=hash)

            # Add user to database and commit
            db.session.add(new_user)

            db.session.commit()

            # Redirect to login
            return redirect(url_for('auth.login'))
        
    return render_template('signup.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))