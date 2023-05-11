import os

from flask import Flask


# from datetime import datetime
# from datetime import timedelta
# from datetime import timezone

from flask_jwt_extended import get_jwt
from flask_jwt_extended import create_access_token, set_access_cookies

# Realize a importação da função que configura a api
from apps.extensions.api import configure_api
from apps.extensions.config import config
from apps.extensions.db import db
from apps.extensions.jwt import configure_jwt
from apps.users.commands import createsuperuser


def create_app(testing=None):
    app = Flask('api-users')

    config_name = os.getenv("FLASK_ENV")
    if testing:
        app.config.from_object('testing')
    else:
        app.config.from_object(config[config_name])

    # Configure MongoEngine
    db.init_app(app)

    # Configure JWT
    configure_jwt(app)

    # executa a chamada da função de configuração
    configure_api(app)

    # add command function to cli commands
    app.cli.add_command(createsuperuser)

    # Implicit Refreshing With Cookies¶
    # @app.after_request
    # def refresh_expiring_jwts(response):
    #     try:
    #         exp_timestamp = get_jwt()["exp"]
    #         now = datetime.now(timezone.utc)
    #         target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
    #         if target_timestamp > exp_timestamp:
    #             access_token = create_access_token(identity=get_jwt_identity())
    #             set_access_cookies(response, access_token)
    #         return response
    #     except (RuntimeError, KeyError):
    #         # Case where there is not a valid JWT. Just return the original response
    #         return response

    return app

# app = create_app()
