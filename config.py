class Config:
    DEBUG = False
    TESTING = False

    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'


class TestingConfig(Config):
    TESTING = True

    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
