from flask_wtf import Form
from wtforms import TextField, PasswordField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo

from project.models import User


class LoginForm(Form):
    email = TextField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])


class CreateForm(Form):
    name = TextField('Display Name', validators=[DataRequired()])
    email = TextField('E-Mail', validators=[DataRequired(), Email()])
    role = SelectField('Role', choices=[
        (role, role) for role in User.available_roles
    ])
    password = PasswordField('Password', validators=[DataRequired()])
    password_confirm = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match.')])
