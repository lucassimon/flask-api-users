# -*- coding:utf-8 -*-

# Python

# Flask
from flask import request

# Third
from flask_restful import Resource
from bcrypt import gensalt, hashpw
from mongoengine.errors import NotUniqueError, ValidationError

# Apps
from apps.responses import (
    resp_already_exists,
    resp_exception,
    resp_data_invalid,
    resp_ok
)
from apps.messages import MSG_NO_DATA, MSG_PASSWORD_WRONG, MSG_INVALID_DATA
from apps.messages import MSG_RESOURCE_CREATED

# Local
from .models import User
from .schemas import UserRegistrationSchema, UserSchema
from .utils import check_password_in_signup


class SignUp(Resource):
    def post(self, *args, **kwargs):
        # Inicializo todas as variaveis utilizadas
        req_data = request.get_json() or None
        data, errors, result = None, None, None
        password, confirm_password = None, None
        schema = UserRegistrationSchema()

        # Se meus dados postados forem Nulos retorno uma respota inválida
        if req_data is None:
            return resp_data_invalid('Users', [], msg=MSG_NO_DATA)

        password = req_data.get('password', None)
        confirm_password = req_data.pop('confirm_password', None)

        # verifico através de uma função a senha e a confirmação da senha
        # Se as senhas não são iguais retorno uma respota inválida
        if not check_password_in_signup(password, confirm_password):
            errors = {'password': MSG_PASSWORD_WRONG}
            return resp_data_invalid('Users', errors)

        # Desserialização os dados postados ou melhor meu payload
        data, errors = schema.load(req_data)

        # Se houver erros retorno uma resposta inválida
        if errors:
            return resp_data_invalid('Users', errors)

        # Crio um hash da minha senha
        hashed = hashpw(password.encode('utf-8'), gensalt(12))

        # Salvo meu modelo de usuário com a senha criptografada e email em lower case
        # Qualquer exceção ao salvar o modelo retorno uma resposta em JSON
        # ao invés de levantar uma exception no servidor
        try:
            data['password'] = hashed
            data['email'] = data['email'].lower()
            model = User(**data)
            model.save()

        except NotUniqueError:
            return resp_already_exists('Users', 'fornecedor')

        except ValidationError as e:
            return resp_exception('Users', msg=MSG_INVALID_DATA, description=e)

        except Exception as e:
            return resp_exception('Users', description=e)

        # Realizo um dump dos dados de acordo com o modelo salvo
        schema = UserSchema()
        result = schema.dump(model)

        # Retorno 200 o meu endpoint
        return resp_ok(
            'Users', MSG_RESOURCE_CREATED.format('Usuário'),  data=result.data,
        )
