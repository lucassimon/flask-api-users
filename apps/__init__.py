# -*- coding: utf-8 -*-

from flask import Flask, g
from config import config

# Third

# Realize a importação da função que configura a api
from .api import configure_api
from .db import db
from .jwt import configure_jwt
from .rabbit import connection_rabbit


def create_app(config_name):
    app = Flask('api-users')

    app.config.from_object(config[config_name])

    @app.before_first_request
    def run_on_start():
        if not 'rabbit' in g:
            g.rabbit = connection_rabbit(app.config.get('AMQP_URI'))

    @app.after_request
    def change_headers(response):
        response.headers['X-APP'] = 'Created with love.'
        response.headers['Server'] = 'API Users'
        return response

    @app.teardown_appcontext
    def close_rabbitmq(response):
        conn = g.pop('rabbit', None)

        if conn is not None:
            conn.close()

    # Configure MongoEngine
    db.init_app(app)

    # Configure JWT
    configure_jwt(app)

    # executa a chamada da função de configuração
    configure_api(app)

    return app
