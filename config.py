from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    """Set Flask configuration from .env file."""
    # General Config
    SECRET_KEY = environ.get('SECRET_KEY')
    FLASK_APP = environ.get('FLASK_APP')
    CURR_USER_KEY = environ.get('CURR_USER_KEY')


    # Database
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProdConfig(Config):
    # General Config
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False

    # Database
    SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL")
    SQLALCHEMY_ECHO = False
    
    # Debug Toolbar
    DEBUG_TB_INTERCEPT_REDIRECTS = False


class TestConfig(Config):
    # General Config
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True

    # Database
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI_TEST")
    SQLALCHEMY_ECHO = False

    # Debug Toolbar
    DEBUG_TB_INTERCEPT_REDIRECTS = False