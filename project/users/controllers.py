# Imports

from flask import flash, redirect, render_template, request, url_for, \
    Blueprint, session

from .forms import LoginForm
from project import db
from project.models import User


# Config
user_bp = Blueprint('users', __name__, template_folder='templates')


# routes
@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(name=request.form['username']).first()
            if user is not None and user.authenticate(
                    request.form['password']) and user.role is not 'disabled':
                session.user = user
                flash('You have successfully logged in!', 'notice')
                return redirect(url_for('home.dashboard'))
            else:
                flash('Username or Password is incorrect!', 'danger')
    return render_template('login.html', form=form)


@user_bp.route('/logout')
def logout():
    session.user = None
    flash('You have logged out!', ' notice')
    return redirect(url_for('home.index'))
