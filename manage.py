import unittest
import os

from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from project import app, db

try:
	app.config.from_object(os.environ['APP_SETTINGS'])
except KeyError:
	app.config.from_object('config.DevelopmentConfig')

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Runs the unit tests"""
    tests = unittest.TestLoader().discover('.')
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':
    manager.run()
