# Flask
from flask import request

# Third
from mongoengine.errors import FieldDoesNotExist
from mongoengine.errors import NotUniqueError, ValidationError
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_apispec import marshal_with, doc, use_kwargs
from flask_apispec.views import MethodResource

# Apps
from apps.extensions.responses import resp_ok, resp_exception, resp_data_invalid, resp_already_exists
from apps.extensions.responses import resp_notallowed_user, resp_does_not_exist

from apps.extensions.messages import MSG_RESOURCE_FETCHED_PAGINATED, MSG_RESOURCE_FETCHED
from apps.extensions.messages import MSG_NO_DATA, MSG_RESOURCE_UPDATED, MSG_INVALID_DATA
from apps.extensions.messages import MSG_ALREADY_EXISTS, MSG_RESOURCE_DELETED

# Local
from .models import User, Admin
from .schemas import UserSchema, UserUpdateSchema
from .repositories import AdminMongoRepository
from .exceptions import (
    UserMongoNotUniqueException, UserMongoValidationErrorException,
    UserMongoDoesNotExistException
)
from .commands import GetUserByCpfCnpjCommand


class AdminUserPageList(MethodResource, Resource):

    @doc(description='Listar usuários/customers paginado', tags=['Users'])
    @marshal_with(UserSchema)
    @jwt_required()
    def get(self, page_id=1):
        # inicializa o schema podendo conter varios objetos
        schema = UserSchema(many=True)
        # incializa o page_size sempre com 10
        page_size = 10

        current_user = AdminMongoRepository().get_admin_by_email(get_jwt_identity())

        if not isinstance(current_user, Admin):
            return current_user

        if not (current_user.is_active()):
            return resp_notallowed_user('Users')

        # se enviarmos o page_size como parametro
        if 'page_size' in request.args:
            # verificamos se ele é menor que 1
            if int(request.args.get('page_size')) < 1:
                page_size = 10
            else:
                # fazemos um type cast convertendo para inteiro
                page_size = int(request.args.get('page_size'))

        try:
            pagination = AdminMongoRepository().get_users_with_pagination(page_id=page_id, page_size=page_size)

            # criamos dados extras a serem respondidos
            extra = {
                'page': pagination.page, 'pages': pagination.pages, 'total': pagination.total,
                'params': {'page_size': page_size}
            }

            # fazemos um dump dos objetos pesquisados
            result = schema.dump(pagination.items)

            return resp_ok(
                'Users', MSG_RESOURCE_FETCHED_PAGINATED.format('usuários'),  data=result,
                **extra
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


class AdminUserResourceByCpf(MethodResource, Resource):

    @doc(description='Buscar usuário por cpf ou cnpj', tags=['Users'])
    @marshal_with(UserSchema)
    @jwt_required()
    def get(self, cpf_cnpj):
        try:
            current_user = get_jwt_identity()
            output = GetUserByCpfCnpjCommand.run(current_user=current_user, cpf_cnpj=cpf_cnpj)
            # Retorno 200 o meu endpoint
            response = resp_ok(
                'Users', MSG_RESOURCE_FETCHED.format("Usuário"),  data=output,
            )
            return response

        except UserMongoDoesNotExistException as exc:
            return resp_does_not_exist(resource='users', description=f"usuário")

        except Exception as exc:
            return resp_exception(
                resource='users',
                description='An error occurred',
                msg=exc.__str__()
            )


class AdminUserResource(Resource):
    @jwt_required()
    def get(self, user_id):
        result = None
        schema = UserSchema()
        current_user = AdminMongoRepository().get_user_by_email(get_jwt_identity())

        if not isinstance(current_user, Admin):
            return current_user

        if not (current_user.is_active()) and current_user.is_admin():
            return resp_notallowed_user('Users')

        user = AdminMongoRepository().get_user_by_id(user_id)

        if not isinstance(user, User):
            return user

        result = schema.dump(user)

        return resp_ok(
            'Users', MSG_RESOURCE_FETCHED.format('Usuários'),  data=result
        )

    @jwt_required()
    def put(self, user_id):
        result = None
        schema = UserSchema()
        update_schema = UserUpdateSchema()
        req_data = request.get_json() or None
        email = None
        current_user = AdminMongoRepository().get_user_by_email(get_jwt_identity())

        if not isinstance(current_user, Admin):
            return current_user

        if not (current_user.is_active()) and current_user.is_admin():
            return resp_notallowed_user('Users')

        # Valido se o payload está vazio
        if req_data is None:
            return resp_data_invalid('Users', [], msg=MSG_NO_DATA)

        # Busco o usuário na coleção users pelo seu id
        user = AdminMongoRepository().get_user_by_id(user_id)

        # se não for uma instancia do modelo User retorno uma resposta
        # da requisição http do flask
        if not isinstance(user, User):
            return user

        # carrego meus dados de acordo com o schema de atualização
        try:
            data = update_schema.load(req_data)

        except ValidationError as err:
            return resp_data_invalid('Users', err.messages)

        email = data.get('email', None)

        # Valido se existe um email na coleção de usuários
        if email and AdminMongoRepository().exists_email_in_users(email, user):
            return resp_data_invalid(
                'Users', [{'email': [MSG_ALREADY_EXISTS.format('usuário')]}]
            )

        try:
            user = AdminMongoRepository().update_user(user, data)
            result = schema.dump(user)

            return resp_ok(
                'Users', MSG_RESOURCE_UPDATED.format('Usuário'),  data=result
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

    @jwt_required()
    def delete(self, user_id):
        current_user = AdminMongoRepository().get_user_by_email(get_jwt_identity())

        if not isinstance(current_user, Admin):
            return current_user

        if not (current_user.is_active()) and current_user.is_admin():
            return resp_notallowed_user('Users')

        # Busco o usuário na coleção users pelo seu id
        user = AdminMongoRepository().get_user_by_id(user_id)

        # se não for uma instancia do modelo User retorno uma resposta
        # da requisição http do flask
        if not isinstance(user, User):
            return user

        try:
            AdminMongoRepository().delete_user(user)
            return resp_ok('Users', MSG_RESOURCE_DELETED.format('Usuário'))

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

