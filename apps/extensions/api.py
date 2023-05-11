# -*- coding: utf-8 -*-

# Third
# Importamos as classes API e Resource
from flask_restful import Api, Resource

from apps.users.resources import SignUp
from apps.users.resources_admin import AdminUserPageList, AdminUserResource, AdminUserResourceByCpf
from apps.auth.resources import AuthResource, AuthAdminResource, RefreshTokenResource


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
    api.add_resource(AdminUserPageList, '/admin/users/page/<int:page_id>')
    api.add_resource(AdminUserResource, '/admin/users/<string:user_id>')
    api.add_resource(AdminUserResourceByCpf, '/admin/users/cpf/<string:cpf_cnpj>')

    # rotas para autenticacao
    api.add_resource(AuthResource, '/auth')
    api.add_resource(AuthAdminResource, '/auth/admin')
    api.add_resource(RefreshTokenResource, '/auth/refresh')

    # inicializamos a api com as configurações do flask vinda por parâmetro
    api.init_app(app)
