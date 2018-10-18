# -*- coding: utf-8 -*-

# Flask
from flask import request

# Third
from flask_restful import Resource
from mongoengine.errors import FieldDoesNotExist
from mongoengine.errors import NotUniqueError, ValidationError
from flask_jwt_extended import get_jwt_identity, jwt_required

# Apps
from apps.responses import resp_ok, resp_exception, resp_data_invalid, resp_already_exists
from apps.responses import resp_notallowed_user

from apps.messages import MSG_RESOURCE_FETCHED_PAGINATED, MSG_RESOURCE_FETCHED
from apps.messages import MSG_NO_DATA, MSG_RESOURCE_UPDATED, MSG_INVALID_DATA
from apps.messages import MSG_ALREADY_EXISTS, MSG_RESOURCE_DELETED

# Local
from .models import User
from .schemas import UserSchema, UserUpdateSchema
from .utils import get_user_by_id, exists_email_in_users, get_user_by_email


class AdminUserPageList(Resource):
    @jwt_required
    def get(self, page_id=1):
        # inicializa o schema podendo conter varios objetos
        schema = UserSchema(many=True)
        # incializa o page_size sempre com 10
        page_size = 10

        current_user = get_user_by_email(get_jwt_identity())

        if not isinstance(current_user, User):
            return current_user

        if not (current_user.is_active()) and current_user.is_admin():
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
            # buscamos todos os usuarios da base utilizando o paginate
            users = User.objects().paginate(page_id, page_size)

        except FieldDoesNotExist as e:
            return resp_exception('Users', description=e.__str__())

        except Exception as e:
            return resp_exception('Users', description=e.__str__())

        # criamos dados extras a serem respondidos
        extra = {
            'page': users.page, 'pages': users.pages, 'total': users.total,
            'params': {'page_size': page_size}
        }

        # fazemos um dump dos objetos pesquisados
        result = schema.dump(users.items)

        return resp_ok(
            'Users', MSG_RESOURCE_FETCHED_PAGINATED.format('usuários'),  data=result.data,
            **extra
        )


class AdminUserResource(Resource):
    @jwt_required
    def get(self, user_id):
        result = None
        schema = UserSchema()
        current_user = get_user_by_email(get_jwt_identity())

        if not isinstance(current_user, User):
            return current_user

        if not (current_user.is_active()) and current_user.is_admin():
            return resp_notallowed_user('Users')

        user = get_user_by_id(user_id)

        if not isinstance(user, User):
            return user

        result = schema.dump(user)

        return resp_ok(
            'Users', MSG_RESOURCE_FETCHED.format('Usuários'),  data=result.data
        )

    @jwt_required
    def put(self, user_id):
        result = None
        schema = UserSchema()
        update_schema = UserUpdateSchema()
        req_data = request.get_json() or None
        email = None
        current_user = get_user_by_email(get_jwt_identity())

        if not isinstance(current_user, User):
            return current_user

        if not (current_user.is_active()) and current_user.is_admin():
            return resp_notallowed_user('Users')

        # Valido se o payload está vazio
        if req_data is None:
            return resp_data_invalid('Users', [], msg=MSG_NO_DATA)

        # Busco o usuário na coleção users pelo seu id
        user = get_user_by_id(user_id)

        # se não for uma instancia do modelo User retorno uma resposta
        # da requisição http do flask
        if not isinstance(user, User):
            return user

        # carrego meus dados de acordo com o schema de atualização
        data, errors = update_schema.load(req_data)

        # em caso de erros retorno uma resposta 422 com os erros de
        # validação do schema
        if errors:
            return resp_data_invalid('Users', errors)

        email = data.get('email', None)

        # Valido se existe um email na coleção de usuários
        if email and exists_email_in_users(email, user):
            return resp_data_invalid(
                'Users', [{'email': [MSG_ALREADY_EXISTS.format('usuário')]}]
            )

        try:
            # para cada chave dentro do dados do update schema
            # atribuimos seu valor
            for i in data.keys():
                user[i] = data[i]

            user.save()

        except NotUniqueError:
            return resp_already_exists('Users', 'usuário')

        except ValidationError as e:
            return resp_exception('Users', msg=MSG_INVALID_DATA, description=e.__str__())

        except Exception as e:
            return resp_exception('Users', description=e.__str__())

        result = schema.dump(user)

        return resp_ok(
            'Users', MSG_RESOURCE_UPDATED.format('Usuário'),  data=result.data
        )

    @jwt_required
    def delete(self, user_id):
        current_user = get_user_by_email(get_jwt_identity())

        if not isinstance(current_user, User):
            return current_user

        if not (current_user.is_active()) and current_user.is_admin():
            return resp_notallowed_user('Users')

        # Busco o usuário na coleção users pelo seu id
        user = get_user_by_id(user_id)

        # se não for uma instancia do modelo User retorno uma resposta
        # da requisição http do flask
        if not isinstance(user, User):
            return user

        try:
            user.active = False
            user.save()

        except NotUniqueError:
            return resp_already_exists('Users', 'usuário')

        except ValidationError as e:
            return resp_exception('Users', msg=MSG_INVALID_DATA, description=e.__str__())

        except Exception as e:
            return resp_exception('Users', description=e.__str__())

        return resp_ok('Users', MSG_RESOURCE_DELETED.format('Usuário'))
