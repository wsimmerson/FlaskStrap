# Imports

from hashlib import md5

from flask import flash, redirect, render_template, request, url_for, \
    Blueprint, session

from .forms import LoginForm, CreateForm, UpdatePasswordForm, UpdateForm
from project import db
from project.models import User
from project.auth import login_required, admin_only


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
@login_required
def logout():
    session.clear()
    flash('You have logged out!', 'success')
    return redirect(url_for('home.index'))


@user_bp.route('/create', methods=['GET', 'POST'])
@login_required
@admin_only
def create():
    form = CreateForm(request.form)
    if request.method == 'POST':
        if form.validate():
            user = User.query.filter_by(
                email=request.form['email']).first()
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


@user_bp.route('/profile/<int:userid>', methods=['GET', 'POST'])
@login_required
def profile(userid):
    user = User.query.get(userid)
    email_hash = md5(user.email.encode('utf-8')).hexdigest()
    if session['user_id'] == userid:
        form = UpdatePasswordForm(request.form)
        if request.method == 'POST':
            if form.validate():
                user = User.query.filter_by(id=userid).first()
                if user.authenticate(request.form['old_password']):
                    user.update_password(form.new_password.data)
                    db.session.add(user)
                    db.session.commit()
                    flash('Password has been changed', 'success')
                else:
                    flash('Old Password is incorrect!', 'danger')
        return render_template("profile.html",
                               user=user,
                               email_hash=email_hash,
                               form=form)
    else:
        return render_template("profile.html",
                               user=user,
                               email_hash=email_hash)


@user_bp.route('/edit/<int:userid>', methods=['GET', 'POST'])
@login_required
@admin_only
def edit(userid):
    user = User.query.get(userid)
    form = UpdateForm(request.form, user)
    if request.method == 'POST' and form.validate():
        user.name = form.name.data

        # verify email is only used by this user
        check_email = User.query.filter_by(email=form.email.data).all()
        valid_email = True
        for c in check_email:
            if c.id != userid:
                valid_email = False
        if valid_email:
            user.email = form.email.data

        user.role = form.role.data
        if form.password.data == form.password_confirm.data and len(
                form.password.data) >= 1:
            user.update_password(form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('User has been updated', 'success')

    return render_template("edit.html", form=form)
