from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import json

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    cf = open('config.json', 'r')
    config = json.load(cf)
    cf.close()
    app.config['SECRET_KEY'] = config['SECRET_KEY']

    # Database initialization
    app.config['SQLALCHEMY_DATABASE_URI'] = config['SQLALCHEMY_DATABASE_URI']

    db.init_app(app)

    # Create authorization blueprint
    from auth import auth
    app.register_blueprint(auth)

    # Create main blueprint
    from main import main
    app.register_blueprint(main)

    from admin import admin
    app.register_blueprint(admin)

    # Initiate Login Manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # Import the User model
    from models import User

    # Get the user assoicated with user id.
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
