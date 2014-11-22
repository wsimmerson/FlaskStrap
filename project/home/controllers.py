##############
#   imports  #
##############

from flask import render_template, Blueprint, request, flash, redirect, url_for

from project import db

# CONFIG
home_bp = Blueprint('home', __name__, template_folder='templates')


# routes
@home_bp.route('/')
def home():
    return render_template('index.html')


@home_bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
