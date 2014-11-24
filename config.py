
class BaseConfig:
    DEBUG = False
    SECRET_KEY = 'And now for something completely different'
    SQLALCHEMY_DATABASE_URI = ''


class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db'


class ProductionConfig(BaseConfig):
    DEBUG = False
