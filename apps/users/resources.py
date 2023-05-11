# Python
from dataclasses import asdict
# Flask
from flask import request

# Third
from flask_restful import Resource

# Apps
from .commands import CreateUserCommand
from apps.extensions.responses import (
    resp_already_exists,
    resp_exception,
    resp_data_invalid,
    resp_ok
)
from apps.extensions.messages import MSG_NO_DATA, MSG_PASSWORD_DIDNT_MATCH, MSG_INVALID_DATA
from apps.extensions.messages import MSG_RESOURCE_CREATED

from .exceptions import UserSchemaValidationErrorException, UserMongoNotUniqueException, UserMongoValidationErrorException

class SignUp(Resource):
    def post(self, *args, **kwargs):
        # Inicializo todas as variaveis utilizadas
        payload = request.get_json() or None

        try:
            output = CreateUserCommand.run(payload, *args, **kwargs)
            # Retorno 200 o meu endpoint
            return resp_ok(
                'Users', MSG_RESOURCE_CREATED.format('Usuário'),  data=output,
            )
        except UserSchemaValidationErrorException as exc:
            return resp_data_invalid(
                resource='users',
                errors=exc.errors,
                msg=exc.__str__()
            )

        except UserMongoNotUniqueException as exc:
            return resp_already_exists(resource='users', description=f"usuário")

        except UserMongoValidationErrorException as exc:
            return resp_data_invalid(
                resource='users',
                errors=exc.errors,
                msg=exc.__str__()
            )

        except Exception as exc:
            return resp_exception(
                resource='users',
                description='An error occurred',
                msg=exc.__str__()
            )
