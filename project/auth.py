from functools import wraps
from flask import session, url_for, redirect, flash
from project.models import User


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Login Required!", "danger")
            return redirect(url_for('users.login'))
        return f(*args, **kwargs)
    return decorated_function


def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_user = User.query.filter_by(id=session['user_id']).first()
        if not current_user.isAdmin():
            flash("ACCESS DENIED!", 'danger')
            return redirect(url_for('home.index'))
        return f(*args, **kwargs)
    return decorated_function
