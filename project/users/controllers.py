# Imports

from hashlib import md5

from flask import flash, redirect, render_template, request, url_for, \
    Blueprint, session

from .forms import LoginForm, CreateForm
from project import db
from project.models import User


# Config
user_bp = Blueprint('users', __name__, template_folder='templates',
                    url_prefix='/user')


# routes
@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=request.form['email']).first()
            if user is not None and user.authenticate(
                    request.form['password']) and user.role != 'disabled':
                session['user_id'] = user.id
                session['user_name'] = user.name
                flash('You have successfully logged in!', 'success')
                return redirect(url_for('home.dashboard'))
            else:
                flash('Username or Password is incorrect!', 'danger')
    return render_template('login.html', form=form)


@user_bp.route('/logout')
def logout():
    session.clear()
    flash('You have logged out!', ' notice')
    return redirect(url_for('home.index'))


@user_bp.route('/create', methods=['GET', 'POST'])
def create():
    form = CreateForm(request.form)
    if request.method == 'POST':
        if form.validate():
            user = User.query.filter_by(email=request.form['email']).first()
            if user is None:
                new_user = User(name=form.name.data,
                                email=form.email.data,
                                password=form.password.data,
                                role=form.role.data)
                db.session.add(new_user)
                db.session.commit()
                flash('User created!', 'success')
                return redirect(url_for('home.index'))
            else:
                flash('That email is already in use!', 'danger')
    return render_template("create.html", form=form)


@user_bp.route('profile/<int:userid>')
def profile(userid):
    user = User.query.get(userid)
    email_hash = md5(user.email.encode('utf-8')).hexdigest()
    return render_template("users/profile.html",
                           user=user,
                           email_hash=email_hash)
