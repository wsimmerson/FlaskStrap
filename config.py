import os

class BaseConfig:
    DEBUG = False
    SECRET_KEY = 'And now for something completely different'
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'development.db')


class ProductionConfig(BaseConfig):
    DEBUG = False
