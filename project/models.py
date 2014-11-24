# Imports
from project import db
from werkzeug import check_password_hash, generate_password_hash


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String)
    role = db.Column(db.String, nullable=False)

    available_roles = ['admin', 'user', 'disabled']

    def __init__(self, name, email, password, role):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)
        self.role = role

    def __repr__(self):
        return '<name {}>'.format(self.name)

    def authenticate(self, password_to_check):
        return check_password_hash(self.password, password_to_check)

    def isAdmin(self):
        return self.role == 'admin'
