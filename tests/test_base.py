import unittest

from flask.ext.testing import TestCase
from sqlalchemy import MetaData

from project import app, db
from project.models import User


class BaseTestCase(TestCase):
    """Base test case"""

    def create_app(self):
        app.config.from_object('config.TestConfig')
        return app

    def setUp(self):
        meta = MetaData(db.engine)
        meta.reflect()
        meta.drop_all()

        db.create_all()
        db.session.add(User("admin", "admin@email.com", "admin", "admin"))
        db.session.commit()


class FlaskTestCase(BaseTestCase):
    def test_index(self):
        res = self.client.get('/', content_type='html/text')
        self.assertEqual(res.status_code, 200)

if __name__ == '__main__':
    unittest.main()
