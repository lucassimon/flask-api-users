# -*- coding: utf-8 -*-

from flask_restful import Api, Resource


class Index(Resource):
    def get(self):
        return {'hello': 'world by apps'}


api = Api()


def configure_api(app):
    # register the resources
    api.add_resource(Index, '/')

    api.init_app(app)
