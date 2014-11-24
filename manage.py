import unittest
import os

from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from project import app, db
from project.models import User


migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Runs the unit tests"""
    tests = unittest.TestLoader().discover('.')
    unittest.TextTestRunner(verbosity=2).run(tests)

@manager.command
def seed():
	"""insert default data"""
	print(app.config['SQLALCHEMY_DATABASE_URI'])
	db.session.add(User("admin", "admin@example.com", "admin", "admin"))
	db.session.commit()

if __name__ == '__main__':
    manager.run()
