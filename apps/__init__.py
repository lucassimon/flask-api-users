# -*- coding: utf-8 -*-


from flask import Flask
from config import config


def create_app(config_name):
    app = Flask('api-users')

    app.config.from_object(config[config_name])

    return app
