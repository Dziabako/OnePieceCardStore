from flask import flash, redirect, url_for
from flask_login import current_user, LoginManager
from functools import wraps


login_manager = LoginManager()
login_manager.login_view = "users.login"


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not login_manager._login_disabled:
            if not current_user.is_authenticated or not current_user.is_admin:
                flash('Access denied: You need to be an admin to access this page.')
                return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function
