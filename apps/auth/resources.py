# -*- coding:utf-8 -*-

# Python

# Flask
from flask import request

# Third
from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import jwt_refresh_token_required, get_jwt_identity
from bcrypt import checkpw

# Apps
from apps.users.models import User
from apps.users.schemas import UserSchema
from apps.users.utils import get_user_by_email
from apps.messages import MSG_NO_DATA, MSG_TOKEN_CREATED
from apps.responses import resp_ok, resp_data_invalid, resp_notallowed_user

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

        data, errors = login_schema.load(req_data)

        if errors:
            return resp_data_invalid('Users', errors)

        # Buscamos nosso usuário pelo email
        user = get_user_by_email(data.get('email'))

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
            extras = {
                'token': create_access_token(identity=user.email),
                'refresh': create_refresh_token(identity=user.email)
            }

            result = schema.dump(user)

            return resp_ok(
                'Auth', MSG_TOKEN_CREATED, data=result.data, **extras
            )

        return resp_notallowed_user('Auth')


class RefreshTokenResource(Resource):

    @jwt_refresh_token_required
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
