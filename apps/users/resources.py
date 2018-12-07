# -*- coding:utf-8 -*-

# Python
from datetime import datetime

# Flask
from flask import request, current_app

# Third
from flask_restful import Resource
from bcrypt import gensalt, hashpw
from mongoengine.errors import NotUniqueError, ValidationError
from flask_jwt_extended import create_access_token, create_refresh_token
from jwt import encode as jwt_encode
from jwt import decode as jwt_decode
from dateutil.relativedelta import relativedelta

from jwt.exceptions import (
    ExpiredSignatureError,
    ImmatureSignatureError,
    InvalidAlgorithmError,
    InvalidAudienceError,
    InvalidIssuedAtError,
    InvalidIssuerError,
    InvalidKeyError,
    MissingRequiredClaimError
)

# Apps
from apps.responses import (
    resp_already_exists,
    resp_exception,
    resp_data_invalid,
    resp_ok
)
from apps.messages import MSG_NO_DATA, MSG_PASSWORD_DIDNT_MATCH, MSG_INVALID_DATA
from apps.messages import MSG_RESOURCE_CREATED, MSG_RESOURCE_UPDATED, MSG_TOKEN_EXPIRED
from apps.messages import MSG_RESEND_ACTIVATE_EMAIL
from apps.services.signup import ProducerSignUp

# Local
from .models import User
from .schemas import UserRegistrationSchema, UserSchema
from .utils import check_password_in_signup, get_user_by_id


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
            errors = {'password': MSG_PASSWORD_DIDNT_MATCH}
            return resp_data_invalid('Users', errors)

        # Desserialização os dados postados ou melhor meu payload
        data, errors = schema.load(req_data)

        # Se houver erros retorno uma resposta inválida
        if errors:
            return resp_data_invalid('Users', errors)

        # Crio um hash da minha senha
        hashed = hashpw(password.encode('utf-8'), gensalt(12))

        # Salvo meu modelo de usuário com a senha criptografada e email
        # em lower case
        # Qualquer exceção ao salvar o modelo retorno uma resposta em JSON
        # ao invés de levantar uma exception no servidor
        try:
            data['password'] = hashed
            data['email'] = data['email'].lower()
            model = User(**data)
            model.save()

        except NotUniqueError:
            return resp_already_exists('Users', 'usuário')

        except ValidationError as e:
            return resp_exception('Users', msg=MSG_INVALID_DATA, description=e.__str__())

        except Exception as e:
            return resp_exception('Users', description=e.__str__())

        extras = {
            'token': create_access_token(identity=model.email),
            'refresh': create_refresh_token(identity=model.email)
        }

        # Realizo um dump dos dados de acordo com o modelo salvo
        schema = UserSchema()
        result = schema.dump(model)

        if current_app.config['ENABLE_SIGNUP']:

            try:
                exp = datetime.utcnow() + relativedelta(days=2)
                payload = {'id': '{}'.format(model.id), 'exp': exp}
                confirm_token = jwt_encode(payload, current_app.config['SECRET_KEY'])
                producer = ProducerSignUp(current_app.config['RABBIT_QUEUE_SIGNUP'])
                producer.publish(result.data, confirm_token)

                # TODO: Update true on registration.sent_activate_email on user model
                model.update(registration__sent_activate_email=True)

            except Exception as e:
                # TODO: If any error ocurred send e-mail to admins
                # I will not block the response because the user was saved previously
                # TODO: Log it or capture this exception to sentry
                pass

        # Retorno 200 o meu endpoint
        return resp_ok(
            'Users', MSG_RESOURCE_CREATED.format('Usuário'), data=result.data, **extras
        )


class ConfirmEmail(Resource):
    def get(self, token, *args, **kwargs):
        try:
            payload = jwt_decode(token, current_app.config['SECRET_KEY'])
            user = get_user_by_id(payload.get('id'))
            if not isinstance(user, User):
                return user

        except ExpiredSignatureError as e:
            # TODO: Resend the e-mail activate to queue

            errors = {'token': MSG_TOKEN_EXPIRED}
            return resp_data_invalid('Users', errors, msg=MSG_RESEND_ACTIVATE_EMAIL)

        except (
            InvalidAudienceError, InvalidIssuerError,
            InvalidIssuedAtError, ImmatureSignatureError, InvalidKeyError,
            InvalidAlgorithmError, MissingRequiredClaimError
        ) as e:
            raise e
            # TODO: Invalid token

        except Exception as e:
            # Capture the exception with sentry
            return resp_exception('Users', description=e.__str__())

        try:
            user.update(active=True)

        except Exception as e:
            # Capture the exception with sentry
            return resp_exception('Users', description=e.__str__())

        # Retorno 200 o meu endpoint
        return resp_ok('Users', MSG_RESOURCE_UPDATED.format('Usuário'))
