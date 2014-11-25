#####################
#      IMPORTS      #
#####################

import os

from flask import Flask, render_template, flash
from flask.ext.sqlalchemy import SQLAlchemy

#################
#    config     #
#################

app = Flask(__name__)

try:
    app.config.from_object(os.environ['APP_SETTINGS'])
except KeyError:
    app.config.from_object('config.DevelopmentConfig')

db = SQLAlchemy(app)


###########################
#   register blueprints   #
###########################
from project.users.controllers import user_bp
from project.home.controllers import home_bp

app.register_blueprint(user_bp)
app.register_blueprint(home_bp)


# Basic HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def indernal_error(error):
    db.session.rollback()
    flash(
        "An unexpected error has occured. The administrator has been notified",
        "danger")
    return render_template('500.html'), 500
