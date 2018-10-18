# -*- coding: utf-8 -*-

from flask import Flask
from config import config

# Realize a importação da função que configura a api
from .api import configure_api
from .db import db
from .jwt import configure_jwt


def create_app(config_name):
    app = Flask('api-users')

    app.config.from_object(config[config_name])

    # Configure MongoEngine
    db.init_app(app)

    # Configure JWT
    configure_jwt(app)

    # executa a chamada da função de configuração
    configure_api(app)

    return app
