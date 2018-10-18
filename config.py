# -*- coding: utf-8 -*-

# Python
from os import getenv
from datetime import timedelta


class Config:
    SECRET_KEY = getenv('SECRET_KEY') or 'uma string randômica e gigante'
    APP_PORT = int(getenv('APP_PORT'))
    DEBUG = eval(getenv('DEBUG').title())
    MONGODB_HOST = getenv('MONGODB_URI')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        minutes=int(getenv('JWT_ACCESS_TOKEN_EXPIRES'))
    )
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(
        days=int(getenv('JWT_REFRESH_TOKEN_EXPIRES'))
    )


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
