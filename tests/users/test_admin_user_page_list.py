# -*- coding: utf-8 -*-
from os import getenv
import pytest
from json import dumps, loads

from pymongo import MongoClient

from apps.messages import MSG_RESOURCE_FETCHED_PAGINATED, MSG_EXCEPTION
from apps.responses import resp_data_invalid


class TestAdminUserPageList:

    def setup_method(self):
        self.data = {}
        self.CREATE_ENDPOINT = '/users'
        self.AUTH_ENDPOINT = '/auth'
        self.ENDPOINT = '/admin/users/page/{}'

    def test_page_size_not_in_params_should_be_ten(self, client, mongo):
        resp = client.post(
            self.CREATE_ENDPOINT,
            data=dumps(dict(full_name='teste', email='teste@teste.com', password='123456', confirm_password='123456')),
            content_type='application/json'
        )

        url = '{}'.format(self.ENDPOINT.format(1))

        token = resp.json.get('token')

        headers = {'Authorization': 'Bearer {}'.format(token)}

        resp = client.get(url, content_type='application/json', headers=headers)

        assert resp.status_code == 200
        assert resp.json.get('params').get('page_size') == 10


    def test_page_size_minus_one_should_be_ten(self, client, mongo):
        resp = client.post(
            self.CREATE_ENDPOINT,
            data=dumps(dict(full_name='teste', email='teste@teste.com', password='123456', confirm_password='123456')),
            content_type='application/json'
        )

        token = resp.json.get('token')

        headers = {'Authorization': 'Bearer {}'.format(token)}

        url = '{}?page_size={}'.format(self.ENDPOINT.format(1), -1)

        resp = client.get(url, content_type='application/json', headers=headers)

        assert resp.status_code == 200
        assert resp.json.get('params').get('page_size') == 10

    def test_page_size_tweenty_should_be_tweenty(self, client, mongo):
        resp = client.post(
            self.CREATE_ENDPOINT,
            data=dumps(dict(full_name='teste', email='teste@teste.com', password='123456', confirm_password='123456')),
            content_type='application/json'
        )

        url = '{}?page_size={}'.format(self.ENDPOINT.format(1), 20)

        token = resp.json.get('token')

        headers = {'Authorization': 'Bearer {}'.format(token)}

        resp = client.get(url, content_type='application/json', headers=headers)

        assert resp.status_code == 200
        assert resp.json.get('params').get('page_size') == 20

    def test_responses_exception_field_not_exist(self, client, mongo):
        uri = getenv('MONGODB_URI_TEST')
        dbclient = MongoClient(uri)
        db = dbclient['api-user-test']
        users = db['users']
        users.delete_many({})
        data = dict(foo='bar', full_name='teste', email='teste1@teste.com', password='123456', confirm_password='123456')
        users.insert_one(data)

        resp = client.post(
            self.CREATE_ENDPOINT,
            data=dumps(dict(full_name='teste', email='teste2@teste.com', password='123456', confirm_password='123456')),
            content_type='application/json'
        )

        token = resp.json.get('token')

        headers = {'Authorization': 'Bearer {}'.format(token)}

        resp = client.get(self.ENDPOINT.format(1), content_type='application/json', headers=headers)

        assert resp.status_code == 500
        assert resp.json.get('message') == MSG_EXCEPTION


    def test_responses_ok(self, client, mongo):
        resp = client.post(
            self.CREATE_ENDPOINT,
            data=dumps(dict(full_name='teste', email='teste@teste.com', password='123456', confirm_password='123456')),
            content_type='application/json'
        )

        token = resp.json.get('token')

        headers = {'Authorization': 'Bearer {}'.format(token)}

        resp = client.get(self.ENDPOINT.format(1), content_type='application/json', headers=headers)

        assert resp.status_code == 200
        assert resp.json.get('message') == MSG_RESOURCE_FETCHED_PAGINATED.format('usuários')

    def test_response_has_items_in_data(self, client, mongo):

        resp = client.post(
            self.CREATE_ENDPOINT,
            data=dumps(dict(full_name='teste', email='teste@teste.com', password='123456', confirm_password='123456')),
            content_type='application/json'
        )

        token = resp.json.get('token')

        headers = {'Authorization': 'Bearer {}'.format(token)}

        resp = client.get(self.ENDPOINT.format(1), content_type='application/json', headers=headers)
        data = resp.json.get('data')

        expected = [
            {
                "active": False,
                "cpf_cnpj": "",
                "email": "teste@teste.com",
                "full_name": "teste",
                "id": data[0].get('id')
            }
        ]

        assert data == expected
