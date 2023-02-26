from flask import Blueprint, render_template, redirect, request, url_for, flash, current_app
from flask_login import LoginManager, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from app import db
from admin import Admin_Tools
import logger
from datetime import datetime

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        # Get username and password fields
        username = request.form['username']
        password = request.form['password']

        # Find user with username data
        user = User.query.filter_by(username=username).first()
        # Check if there is a user with that username if so check password
        if user:

            # Get the password hash
            hash = user.password

            # Check the password against hash
            if check_password_hash(hash, password):
                login_user(user)

                logger.Logger.log_general('Logged In:', username)

                # Redirect to profile
                return redirect(url_for('main.profile'))
            
            else:
                flash('Incorrect Password')

        else:
            flash('User Not Found')

    return render_template('login.html')

@auth.route('/signup/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        logger.Logger.log_general('Post signup')

        # Get username, password, and name.
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']

        # Query for other users
        check_users = User.query.filter_by(username=username).first()

        # Good to continue if no other users with this username
        if not check_users:
            if username:
                if password:
                    if name:

                        # Generate password hash and create new User entry
                        hash = generate_password_hash(password, method='sha256')
                        new_user = User(username=username, name=name, password=hash)

                        # Add user to database and commit
                        db.session.add(new_user)

                        db.session.commit()

                        logger.Logger.log_general('Signed Up:', username, hash, name)

                        # Redirect to login
                        return redirect(url_for('auth.login'))
                    
                    else:
                        flash('Provide A Name')

                else:
                    flash('Provide A Password')

            else:
                flash('Provide A Username')

        else:
            flash('Username Taken')
        
    logger.Logger.log_general('Rendering signup')
    return render_template('signup.html')

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))