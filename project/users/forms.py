from flask_wtf import Form
from wtforms import TextField, PasswordField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo

from project.models import User


class LoginForm(Form):
    email = TextField('E-mail', validators=[
        DataRequired(message='Email is required!'),
        Email()])
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required!')])


class CreateForm(Form):
    name = TextField('Display Name', validators=[
        DataRequired(message='Display Name is required!')])
    email = TextField('E-Mail', validators=[
        DataRequired(message='Email is required'),
        Email()])
    role = SelectField('Role', choices=[
        (role, role) for role in User.available_roles
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required!')])
    password_confirm = PasswordField('Confirm Password', validators=[
        DataRequired(message='Password must be confirmed'),
        EqualTo('password', message='Passwords must match.')])


class UpdatePasswordForm(Form):
    old_password = PasswordField('Old Password', validators=[
        DataRequired(message='Password is required!')])
    new_password = PasswordField('New Password', validators=[
        DataRequired(message='New Password is required')])
    confirm_new_password = PasswordField('Confirm New Password', validators=[
        DataRequired(message='Massword must be confirmed.'),
        EqualTo('new_password', message='Passwords must match.')])
