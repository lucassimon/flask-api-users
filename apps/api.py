# -*- coding: utf-8 -*-

# Third
# Importamos as classes API e Resource
from flask_restful import Api, Resource

from apps.users.resources import SignUp
from apps.users.resources_admin import AdminUserPageList


# Criamos uma classe que extende de Resource
class Index(Resource):

    # Definimos a operação get do protocolo http
    def get(self):

        # retornamos um simples dicionário que será automáticamente
        # retornado em json pelo flask
        return {'hello': 'world by apps'}


# Instânciamos a API do FlaskRestful
api = Api()


def configure_api(app):

    api.add_resource(Index, '/')

    # rotas para o endpoint de usuarios
    api.add_resource(SignUp, '/users')

    # rotas para os admins
    api.add_resource(AdminUserPageList, '/admin/users/<int:page_id>')

    # inicializamos a api com as configurações do flask vinda por parâmetro
    api.init_app(app)
