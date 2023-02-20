from flask import Blueprint, render_template, redirect, request, url_for, flash, current_app
from flask_login import LoginManager, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from app import db
from admin import Admin_Tools
import logging
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

                # Redirect to profile
                return redirect(url_for('main.profile'))
            
            else:
                flash('Incorrect Password')

        else:
            flash('User Not Found')

    return render_template('login.html')

@auth.route('/signup', methods=['GET'])
def signup()

@auth.route('/commit_signup/', methods=['POST'])
def commit_signup():
    logging.basicConfig(filename='debug.log', level=logging.DEBUG)
    logging.debug(datetime.now())
    logging.debug('Signup page active, POST request recieved')
    logging.debug('Using Database URI: %s' % (current_app.config['SQLALCHEMY_DATABASE_URI']))
    # Get username, password, and name.
    username = request.form['username']
    password = request.form['password']
    name = request.form['name']

    logging.debug('Recieved: Username %s, Password %s, Name %s' % (username, password, name))

    # Query for other users
    check_users = User.query.filter_by(username=username).first()

    # Good to continue if no other users with this username
    if not check_users:
        if username:
            if password:
                if name:

                    logging.debug('Valid submission attempting to commit to db')

                    # Generate password hash and create new User entry
                    hash = generate_password_hash(password, method='sha256')
                    new_user = User(username=username, name=name, password=hash)

                    # Add user to database and commit
                    db.session.add(new_user)

                    logging.debug('New user added to session')

                    db.session.commit()

                    logging.debug('Session committed to database, ')

                    # Redirect to login
                    return redirect(url_for('auth.login'))
                
                else:
                    logging.debug('Did not provide name')
                    flash('Provide A Name')

            else:
                logging.debug('Did not provide password')
                flash('Provide A Password')

        else:
            logging.debug('Did not provide password')
            flash('Provide A Username')

    else:
        logging.debug('Found users with username: %s' % (check_users.username))
        flash('Username Taken')
    
    return redirect(url_for('auth.signup'))

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))