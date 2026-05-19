from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
migrate = Migrate()

login_manager.login_view = 'auth.login'
login_manager.login_message = ''

def verified_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return login_manager.unauthorized()
        if not current_user.email_verified:
            flash('Please verify your email address before accessing this page.', 'warning')
            return redirect(url_for('user.profile'))
        return f(*args, **kwargs)
    return decorated_function
