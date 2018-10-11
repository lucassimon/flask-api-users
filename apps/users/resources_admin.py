# -*- coding: utf-8 -*-

# Flask
from flask import request

# Third
from flask_restful import Resource
from mongoengine.errors import FieldDoesNotExist

# Apps
from apps.responses import resp_ok, resp_exception

from apps.messages import MSG_RESOURCE_FETCHED_PAGINATED

# Local
from .models import User
from .schemas import UserSchema


class AdminUserPageList(Resource):

    def get(self, page_id=1):
        # inicializa o schema podendo conter varios objetos
        schema = UserSchema(many=True)
        # incializa o page_size sempre com 10
        page_size = 10

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
