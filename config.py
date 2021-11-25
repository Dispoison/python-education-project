"""Project config module"""

from os import environ


env = {'production': 'config.ProductionConfig',
       'development': 'config.DevelopmentConfig',
       'testing': 'config.TestingConfig',
       'default': 'config.ProductionConfig'}


class Config:
    """Base config"""
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'secret_key'
    RESTX_MASK_SWAGGER = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    """Config used in production"""
    SECRET_KEY = environ.get('SECRET_KEY')

    DB_USER = environ.get('DB_USER')
    DB_PASSWORD = environ.get('DB_PASSWORD')
    DB_HOST = environ.get('DB_HOST')
    DB_PORT = environ.get('DB_PORT')
    DB_NAME = environ.get('DB_NAME')

    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'


class DevelopmentConfig(Config):
    """Config used in development"""
    ENV = 'development'
    DEBUG = True
    DB_USER = environ.get('DB_USER')
    DB_PASSWORD = environ.get('DB_PASSWORD')
    DB_HOST = environ.get('DB_HOST')
    DB_PORT = environ.get('DB_PORT')
    DB_NAME = environ.get('DB_NAME')

    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'


class TestingConfig(Config):
    """Config used in testing"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
