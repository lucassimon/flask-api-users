# Flask

from flask import jsonify

# Third
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token, create_refresh_token
# Apps
from apps.users.models import User

# Local
from .messages import MSG_INVALID_CREDENTIALS, MSG_TOKEN_EXPIRED

def create_tokens(output, additional_claims={'group': 'users'}, logger=None):
    token = create_access_token(identity=output["email"], additional_claims=additional_claims)
    refresh_token = create_refresh_token(identity=output["email"])

    if logger:
        logger.info("auth.user.command", message="Creating jwt tokens")

    return {
        'token': token,
        'refresh': refresh_token
    }

def configure_jwt(app):

    # Add jwt handler
    jwt = JWTManager(app)

    @jwt.additional_claims_loader
    def add_claims_to_access_token(identity):
        return {
            "aud": "some_audience",
            "foo": "bar",
        }

    @jwt.expired_token_loader
    def my_expired_token_callback():
        resp = jsonify({
            'status': 401,
            'sub_status': 42,
            'message': MSG_TOKEN_EXPIRED
        })

        resp.status_code = 401

        return resp

    @jwt.unauthorized_loader
    def my_unauthorized_callback(e):
        resp = jsonify({
            'status': 401,
            'sub_status': 1,
            'description': e,
            'message': MSG_INVALID_CREDENTIALS
        })

        resp.status_code = 401

        return resp

    # @jwt.claims_verification_loader
    # def my_claims_verification_callback(e):
    #     resp = jsonify({
    #         'status': 401,
    #         'sub_status': 2,
    #         'description': e,
    #         'message': MSG_INVALID_CREDENTIALS
    #     })

    #     resp.status_code = 401

    #     return resp

    @jwt.invalid_token_loader
    def my_invalid_token_loader_callback(e):
        resp = jsonify({
            'status': 401,
            'sub_status': 3,
            'description': e,
            'message': MSG_INVALID_CREDENTIALS
        })

        resp.status_code = 401

        return resp

    @jwt.needs_fresh_token_loader
    def my_needs_fresh_token_callback(e):
        resp = jsonify({
            'status': 401,
            'sub_status': 4,
            'description': e,
            'message': MSG_INVALID_CREDENTIALS
        })

        resp.status_code = 401

        return resp

    @jwt.revoked_token_loader
    def my_revoked_token_callback(e):
        resp = jsonify({
            'status': 401,
            'sub_status': 5,
            'description': e,
            'message': MSG_INVALID_CREDENTIALS
        })

        resp.status_code = 401

        return resp

    # @jwt.user_loader_callback_loader
    # def my_user_loader_callback(e):
    #     resp = jsonify({
    #         'status': 401,
    #         'sub_status': 6,
    #         'description': e,
    #         'message': MSG_INVALID_CREDENTIALS
    #     })

    #     resp.status_code = 401

    #     return resp

    # @jwt.user_loader_error_loader
    # def my_user_loader_error_callback(e):
    #     resp = jsonify({
    #         'status': 401,
    #         'sub_status': 7,
    #         'description': e,
    #         'message': MSG_INVALID_CREDENTIALS
    #     })

    #     resp.status_code = 401

    #     return resp

    # @jwt.token_in_blacklist_loader
    # def my_token_in_blacklist_callback(e):
    #     resp = jsonify({
    #         'status': 401,
    #         'sub_status': 8,
    #         'description': e,
    #         'message': MSG_INVALID_CREDENTIALS
    #     })

    #     resp.status_code = 401

    #     return resp

    # @jwt.claims_verification_failed_loader
    # def my_claims_verification_failed_callback(e):
    #     resp = jsonify({
    #         'status': 401,
    #         'sub_status': 9,
    #         'description': e,
    #         'message': MSG_INVALID_CREDENTIALS
    #     })

    #     resp.status_code = 401

    #     return resp
