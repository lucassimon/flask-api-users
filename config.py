# -*- coding: utf-8 -*-

# Python
from os import getenv


class Config:
    SECRET_KEY = getenv('SECRET_KEY') or 'uma string randômica e gigante'
    APP_PORT = int(getenv('APP_PORT'))
    DEBUG = eval(getenv('DEBUG').title())
    MONGODB_HOST = getenv('MONGODB_URI')


class DevelopmentConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True


class TestingConfig(Config):
    FLASK_ENV = 'testing'
    TESTING = True
    MONGODB_HOST = getenv('MONGODB_URI_TEST')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
