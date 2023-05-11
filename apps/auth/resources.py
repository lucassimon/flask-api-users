# Python

# Flask
from flask import request

# Third
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required, get_jwt_identity, set_access_cookies

# Apps
from apps.extensions.messages import MSG_TOKEN_CREATED
from apps.extensions.responses import resp_ok, resp_data_invalid, resp_does_not_exist, resp_exception
from apps.users.exceptions import UserMongoDoesNotExistException
# Local
from .commands import AuthUsersCommand, AuthAdminUsersCommand
from .exceptions import LoginSchemaValidationErrorException


class AuthAdminResource(Resource):
    def post(self, *args, **kwargs):
        '''
        Route to do login in API
        '''
        # Inicializo todas as variaveis utilizadas
        payload = request.get_json() or None

        try:
            output = AuthAdminUsersCommand.run(payload, *args, **kwargs)
            # Retorno 200 o meu endpoint
            response = resp_ok(
                'Users', MSG_TOKEN_CREATED.format('usuário'),  data=output,
            )
            # set_access_cookies(response=response)
            return response

        except LoginSchemaValidationErrorException as exc:
            return resp_data_invalid(
                resource='users',
                errors=exc.errors,
                msg=exc.__str__()
            )

        except UserMongoDoesNotExistException as exc:
            return resp_does_not_exist(resource='users', description=f"usuário")

        except Exception as exc:
            return resp_exception(
                resource='users',
                description='An error occurred',
                msg=exc.__str__()
            )


class AuthResource(Resource):
    def post(self, *args, **kwargs):
        '''
        Route to do login in API
        '''
        # Inicializo todas as variaveis utilizadas
        payload = request.get_json() or None

        try:
            output = AuthUsersCommand.run(payload, *args, **kwargs)
            # Retorno 200 o meu endpoint
            return resp_ok(
                'Users', MSG_TOKEN_CREATED,  data=output,
            )

        except LoginSchemaValidationErrorException as exc:
            return resp_data_invalid(
                resource='users',
                errors=exc.errors,
                msg=exc.__str__()
            )

        except UserMongoDoesNotExistException as exc:
            return resp_does_not_exist(resource='users', description=f"usuário")

        except Exception as exc:
            return resp_exception(
                resource='users',
                description='An error occurred',
                msg=exc.__str__()
            )


class RefreshTokenResource(Resource):
    @jwt_required(refresh=True)
    def post(self, *args, **kwargs):
        '''
        Refresh a token that expired.

        http://flask-jwt-extended.readthedocs.io/en/latest/refresh_tokens.html
        '''
        extras = {
            'token': create_access_token(identity=get_jwt_identity()),
        }

        return resp_ok(
            'Auth', MSG_TOKEN_CREATED, **extras
        )
