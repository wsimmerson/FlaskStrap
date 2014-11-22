#####################
#      IMPORTS      #
#####################

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os

#################
#    config     #
#################

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)


###########################
#   register blueprints   #
###########################
from project.users.controllers import user_bp
from project.home.controllers import home_bp

app.register_blueprint(user_bp)
app.register_blueprint(home_bp)


#####################
#   import models   #
#####################
