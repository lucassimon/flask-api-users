# -*- coding:utf-8 -*-

# Python

# Flask
from flask import request

# Third
from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import jwt_required, get_jwt_identity, set_access_cookies
from bcrypt import checkpw
from marshmallow import ValidationError

# Apps
from apps.users.models import User
from apps.users.schemas import UserSchema
from apps.users.repositories import UserMongoRepository
from apps.extensions.messages import MSG_NO_DATA, MSG_TOKEN_CREATED
from apps.extensions.responses import resp_ok, resp_data_invalid, resp_notallowed_user

# Local
from .schemas import LoginSchema


class AuthResource(Resource):
    def post(self, *args, **kwargs):
        '''
        Route to do login in API
        '''
        req_data = request.get_json() or None
        user = None
        login_schema = LoginSchema()
        schema = UserSchema()

        if req_data is None:
            return resp_data_invalid('Users', [], msg=MSG_NO_DATA)

        # Desserialização os dados postados ou melhor meu payload
        try:
            data = login_schema.load(req_data)
        except ValidationError as err:
            print(err.messages)  # => {"email": ['"foo" is not a valid email address.']}
            print(err.valid_data)  # => {"name": "John"}

            # Se houver erros retorno uma resposta inválida
            if err:
                return resp_data_invalid('Users', err)

        # Buscamos nosso usuário pelo email
        user = UserMongoRepository().get_user_by_email(data.get('email'))

        # Em caso de exceção ou não é uma instancia do Modelo de User
        # retornamos a resposta
        if not isinstance(user, User):
            return user

        # Verificamos se o usuário está ativo na plataforma. Se não ele
        # não podera autenticar e não ter acesso a nada
        if not user.is_active():
            return resp_notallowed_user('Auth')

        # Conferimos a senha informada no payload de dados com a senha cadastrada
        # em nosso banco.
        if checkpw(data.get('password').encode('utf-8'), user.password.encode('utf-8')):

            # Chamamos os metodos para criar os tokens passando como identidade
            # o email do nosso usuario
            access_token = create_access_token(identity=user.email)
            extras = {
                'token': access_token,
                'refresh': create_refresh_token(identity=user.email)
            }

            result = schema.dump(user)

            response = resp_ok(
                'Auth', MSG_TOKEN_CREATED, data=result, **extras
            )

            # set_access_cookies(response, access_token)
            return response

        return resp_notallowed_user('Auth')


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
