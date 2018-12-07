# -*- coding: utf-8 -*-

from flask import Flask
from config import config

# Third

# Realize a importação da função que configura a api
from .api import configure_api
from .db import db
from .jwt import configure_jwt

from .sentry import configure_sentry


def create_app(config_name):
    app = Flask('api-users')

    app.config.from_object(config[config_name])

    @app.after_request
    def change_headers(response):
        response.headers['X-APP'] = 'Created with love.'
        response.headers['Server'] = 'API Users'
        return response

    # Configure MongoEngine
    db.init_app(app)

    # Configure JWT
    configure_jwt(app)

    # executa a chamada da função de configuração
    configure_api(app)

    # configura o sentry
    configure_sentry(app.config.get('SENTRY_DSN'))

    return app
