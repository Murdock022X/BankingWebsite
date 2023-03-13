from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import json
import os
from pathlib import Path

db = SQLAlchemy()

def create_app():
    """Creates the app and defines several important aspects of the app 
    including database configuration, secret key, a Path object with the 
    project root, blueprint routes for the app, the login manager and how 
    to load users.

    Returns:
        Flask: The initialized flask app object.
    """    
    # Initialize app
    app = Flask(__name__)

    # Load configuration
    cf = open('app_config.json', 'r')
    config = json.load(cf)
    cf.close()

    # Initialize secret key in app config.
    app.config['SECRET_KEY'] = config['SECRET_KEY']

    # Initialize sqlalchemy database uri in app config.
    app.config['SQLALCHEMY_DATABASE_URI'] = config['SQLALCHEMY_DATABASE_URI']

    app.config['PROJECT_ROOT'] = Path(os.path.realpath(os.path.dirname(__file__)))

    # Initialize app
    db.init_app(app)

    # Create authorization blueprint
    from auth import auth
    app.register_blueprint(auth)

    # Create main blueprint
    from main import main
    app.register_blueprint(main)

    # Create admin blueprint
    from admin import admin
    app.register_blueprint(admin)

    # Initiate Login Manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    login_manager.login_message_category = "info"

    # Import the User model
    from models import User

    # Get the user assoicated with user id.
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
