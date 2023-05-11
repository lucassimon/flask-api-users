# -*- coding: utf-8 -*-

# Python
from os import getenv
from datetime import timedelta


class Config:
    SECRET_KEY = getenv('SECRET_KEY')
    PORT = int(getenv('PORT', 8080))
    DEBUG = getenv('DEBUG') or False
    MONGODB_HOST = getenv('MONGODB_URI', 'mongodb://0.0.0.0:27017/api-users')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        minutes=int(getenv('JWT_ACCESS_TOKEN_EXPIRES', 20))
    )
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(
        days=int(getenv('JWT_REFRESH_TOKEN_EXPIRES', 30))
    )


class DevelopmentConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True


class TestingConfig(Config):
    FLASK_ENV = 'testing'
    TESTING = True
    MONGODB_HOST = getenv('MONGODB_URI_TEST')


class ProductionConfig(Config):
    FLASK_ENV = 'production'
    TESTING = False
    DEBUG = False


config = {
    'production': ProductionConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
