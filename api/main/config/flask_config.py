import os
from dotenv import load_dotenv

# Loading environment variables
load_dotenv()

DB_TYPE = os.getenv('DATABASE_TYPE')
DB_USERNAME = os.getenv('MYSQL_USER')
DB_ROOT_PASSWORD = os.getenv('MYSQL_ROOT_PASSWORD')
DB_SERVER = os.getenv('DATABASE_SERVER')
DB_NAME = os.getenv('MYSQL_DATABASE')




class Config(object):
    """Base config, uses staging database server."""
    SQLALCHEMY_DATABASE_URI = str(DB_TYPE) + str(DB_USERNAME) + ":" + str(DB_ROOT_PASSWORD) + "@" + str(DB_SERVER) + "/" + str(DB_NAME)
    SQLALCHEMY_TRACK_MODIFICATIONS = bool(os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS'))
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = os.getenv('MAIL_PORT')
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_SENDER = os.getenv('MAIL_SENDER')
    MAIL_SUPPRESS_SEND = os.getenv('MAIL_SUPPRESS_SEND')

# This classes heredate from Config
class ProductionConfig(Config):
    """Uses production database server."""


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    DEBUG = True
