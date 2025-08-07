from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from config import config

# Инициализация расширений
db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_name=None):
    """Flask application factory"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    # Add built-in functions to Jinja2 environment
    app.jinja_env.globals.update(min=min, max=max, abs=abs, round=round, len=len)
    
    # Register blueprints
    from app.routes import main, auth
    app.register_blueprint(main)
    app.register_blueprint(auth)
    
    # Create tables in app context
    with app.app_context():
        db.create_all()
    
    return app

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.get(int(user_id))
