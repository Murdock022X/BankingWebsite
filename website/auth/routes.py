from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from website.models import User, db
from website.auth.forms import SignupForm, LoginForm
from website.utils.flash_codes import flash_codes

# Create the authorization blueprint, should be used for routes that 
# have to do with user management.
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """A page used to login users.

    Returns:
        str/response: Returns an html string in the case of a get request or 
        a post request that isn't successful at logging in. In the case of 
        a successful post request a redirect response is sent. 
    """    

    flash_offset = 13

    # Create the login form.
    form = LoginForm()

    # Check if the form has been validated and submitted.
    if form.validate_on_submit():

        # Find user with username data
        user = User.query.filter_by(username=form.username.data).first()

        # Check if there is a user with that username if so check password
        if user:
            
            # Get the password hash
            hash = user.password

            # Check the password against hash
            if check_password_hash(hash, form.password.data):
                # Login the user.
                login_user(user)

                # Flash that the user has logged in.
                flash_codes(flash_code='2', flash_offset=flash_offset)

                # Redirect to profile
                return redirect(url_for('main.profile'))
            
            else:
                flash_codes(flash_code='1', flash_offset=flash_offset)

        else:
            flash_codes(flash_code='0', flash_offset=flash_offset)

    # Return the rendered template for login.html.
    return render_template('login.html', form=form)


@auth.route('/signup/', methods=['GET', 'POST'])
def signup():
    """The signup page used to create new user accounts.

    Returns:
        str/response: Returns an html string in the case of a get request or 
        a post request that isn't successful at signing up. In the case of 
        a successful post request a redirect response is sent.
    """    

    flash_offset = 16

    # Create the signup form.
    form = SignupForm()

    # Check if the form has been validated and submitted.
    if form.validate_on_submit():

        # Query for other users with same username.
        check_users = User.query.filter_by(username=form.username.data).first()

        # Good to continue if no other users with this username
        if not check_users:

            # Generate password hash and create new User entry
            hash = generate_password_hash(form.password.data, method='sha256')
            new_user = User(username=form.username.data, name=form.name.data, password=hash)

            # Add user to database and commit
            db.session.add(new_user)

            db.session.commit()

            flash_codes(flash_code='1', flash_offset=flash_offset)

            # Redirect to login
            return redirect(url_for('auth.login'))
        
        else:
            flash_codes(flash_code='0', flash_offset=flash_offset)
        
    # Return the rendered html page.
    return render_template('signup.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    """Logout the current user.

    Returns:
        response: A redirect response to the home page.
    """    

    # Logout current user.
    logout_user()

    flash_codes(flash_code='0', flash_offset=18)

    # Redirect to main.home.
    return redirect(url_for('main.home'))