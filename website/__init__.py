from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import json
import os
from pathlib import Path

# Initialize the login manager and Sqlalchemy database.
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = "danger"

def create_app():
    """Create the instance of our flask app, setting up relevant 
    configurations, login manager, database uri, and flask blueprints.

    Returns:
        Flask: The flask app instance that is created.
    """    
    app = Flask(__name__)
    
    # Store path to project root.
    app.config['PROJECT_ROOT'] = Path(os.path.realpath(os.path.dirname(__file__)))

    # Load configuration
    cf = open(str(app.config['PROJECT_ROOT'] / Path('configs/app_config.json')), 'r')
    config = json.load(cf)
    cf.close()

    # Initialize secret key in app config.
    app.config['SECRET_KEY'] = config['SECRET_KEY']

    # Initialize sqlalchemy database uri in app config.
    app.config['SQLALCHEMY_DATABASE_URI'] = config['SQLALCHEMY_DATABASE_URI']

    # Loads app error codes.
    flash_config = open(str(app.config['PROJECT_ROOT'] / Path('configs/flash_codes.json')), 'r')
    app.config['FLASH_CODES'] = json.load(flash_config)
    flash_config.close()

    # Initialize database and login managers to be connected to app.
    db.init_app(app=app)
    login_manager.init_app(app=app)

    # Create authorization blueprint
    from website.auth.routes import auth
    app.register_blueprint(auth)

    # Create main blueprint
    from website.main.routes import main
    app.register_blueprint(main)

    # Create admin blueprint
    from website.admin.routes import admin
    app.register_blueprint(admin)
    
    return app