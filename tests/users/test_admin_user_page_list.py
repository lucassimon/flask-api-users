# -*- coding: utf-8 -*-
from os import getenv
import pytest
from json import dumps, loads
from unittest import mock

from pymongo import MongoClient
from mongoengine.errors import FieldDoesNotExist

from apps.extensions.messages import MSG_RESOURCE_FETCHED_PAGINATED, MSG_EXCEPTION
from apps.extensions.responses import resp_data_invalid
from apps.users.models import User
from tests.factories.users import UserFactory

# https://stackabuse.com/guide-to-flask-mongoengine-in-python/

class TestAdminUserPageList:

    def setup_method(self):
        self.data = {}
        self.CREATE_ENDPOINT = '/users'
        self.AUTH_ENDPOINT = '/auth'
        self.ENDPOINT = '/admin/users/page/{}'

    def teardown_method(self):
        User.objects.delete()

    def test_response_params_should_be_ten(self, client, auth, mongo):

        url = '{}'.format(self.ENDPOINT.format(1))
        headers = {"Authorization": f"Bearer {client.access_token}"}

        resp = client.get(url, content_type='application/json', headers=headers)

        assert resp.status_code == 200
        assert resp.json.get('params').get('page_size') == 10


    def test_page_size_is_zero_should_returns_ten(self, client, auth, mongo):
        url = '{}?page_size={}'.format(self.ENDPOINT.format(1), -1)
        headers = {"Authorization": f"Bearer {client.access_token}"}

        resp = client.get(url, content_type='application/json', headers=headers)

        assert resp.status_code == 200
        assert resp.json.get('params').get('page_size') == 10

    def test_set_page_size_tweenty_should_returns_tweenty(self, client, auth, mongo):
        url = '{}?page_size={}'.format(self.ENDPOINT.format(1), 20)
        headers = {"Authorization": f"Bearer {client.access_token}"}

        resp = client.get(url, content_type='application/json', headers=headers)

        assert resp.status_code == 200
        assert resp.json.get('params').get('page_size') == 20

    @mock.patch("apps.users.repositories.User.objects")
    def test_responses_exception_field_not_exist(self, UserMock, client, auth, mongo):
        UserMock.side_effect = Exception(MSG_EXCEPTION)

        headers = {"Authorization": f"Bearer {client.access_token}"}
        resp = client.get(self.ENDPOINT.format(1), content_type='application/json', headers=headers)

        assert resp.status_code == 500
        assert resp.json.get('message') == MSG_EXCEPTION


    def test_responses_ok(self, client, auth, mongo):
        headers = {"Authorization": f"Bearer {client.access_token}"}
        resp = client.get(self.ENDPOINT.format(1), content_type='application/json', headers=headers)

        assert resp.status_code == 200
        assert resp.json.get('message') == MSG_RESOURCE_FETCHED_PAGINATED.format('usuários')

    def test_response_has_items_in_data(self, client, auth, mongo):
        user = UserFactory.create(full_name='teste', email='teste@teste.com', cpf_cnpj='some-cpf', date_of_birth='2010-11-12')
        headers = {"Authorization": f"Bearer {client.access_token}"}
        resp = client.get(self.ENDPOINT.format(1), content_type='application/json', headers=headers)
        data = resp.json.get('data')

        expected = [
            {
                "active": user.active,
                "cpf_cnpj": user.cpf_cnpj,
                "email": user.email,
                "full_name": user.full_name,
                "date_of_birth": user.date_of_birth,
                "id": data[0].get("id")
            }
        ]

        assert data == expected

    def test_response_items_paginated(self, client, auth, mongo):
        users = UserFactory.create_batch(4)
        headers = {"Authorization": f"Bearer {client.access_token}"}
        url = '{}?page_size={}'.format(self.ENDPOINT.format(1), 1)
        resp = client.get(url, content_type='application/json', headers=headers)
        data = resp.json.get('data')

        expected = [
            {
                "active": users[0].active,
                "cpf_cnpj": users[0].cpf_cnpj,
                "email": users[0].email,
                "full_name": users[0].full_name,
                "date_of_birth": users[0].date_of_birth,
                "id": data[0].get("id")
            }
        ]

        assert data == expected


        url = '{}?page_size={}'.format(self.ENDPOINT.format(2), 1)
        resp = client.get(url, content_type='application/json', headers=headers)
        data = resp.json.get('data')

        expected = [
            {
                "active": users[1].active,
                "cpf_cnpj": users[1].cpf_cnpj,
                "email": users[1].email,
                "full_name": users[1].full_name,
                "date_of_birth": users[1].date_of_birth,
                "id": data[0].get("id")
            }
        ]

        assert data == expected
