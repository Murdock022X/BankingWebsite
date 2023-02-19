from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
app = Flask(__name__)

app.config['SECRET_KEY'] = 'SPQR'

# Database initialization
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bank_data.db'

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
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

# Import the User model
from models import User

# Get the user assoicated with user id.
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

