from functools import wraps
from flask import session, url_for, redirect, flash


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Login Required!", "danger")
            return redirect(url_for('users.login'))
        return f(*args, **kwargs)
    return decorated_function
