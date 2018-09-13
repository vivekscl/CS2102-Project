import os
# from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
# use this .env file to store confidential configurations such as
# heroku config, API keys and remember to put .env into .gitignore
# load_dotenv(os.path.join(basedir, '.env'))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', os.urandom(24))
    DEBUG = False
    TESTING = False
    SCHEMA_LOCATION = os.environ.get('DEV_SCHEMA_LOCATION', os.path.join(basedir, 'db/schema.sql'))
    CONNECTION_FILE = open('conn.txt', 'r').read()

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_NAME = os.environ.get('DEV_DATABASE_NAME', "cs2102")


class TestingConfig(Config):
    TESTING = True
    DATABASE_NAME = os.environ.get('TEST_DATABASE_NAME', "testdb")


class ProductionConfig(Config):
    pass
    # (TODO)Set schema location and env for production here


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
