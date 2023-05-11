# -*- coding: utf-8 -*-
import pytest
import mongomock
from unittest import mock
from mongoengine.errors import NotUniqueError, ValidationError

from json import dumps, loads

from apps.extensions.messages import MSG_NO_DATA, MSG_INVALID_DATA, MSG_PASSWORD_DIDNT_MATCH
from apps.extensions.messages import MSG_FIELD_REQUIRED, MSG_RESOURCE_CREATED, MSG_ALREADY_EXISTS
from apps.extensions.responses import resp_data_invalid
from apps.users.models import User

class TestSignUp:

    def setup_method(self):
        self.data = {}
        self.ENDPOINT = '/users'

    def teardown_method(self):
        User.objects.delete()

    def test_response_422_when_empty_payload(self, client):
        resp = client.post(
            self.ENDPOINT,
            json={},
            content_type='application/json'
        )
        assert resp.status_code == 422
        assert resp.json.get('message') == 'The input data is wrong'

    def test_response_422_when_data_is_not_valid(self, client):
        resp = client.post(
            self.ENDPOINT,
            json=dict(foo='bar'),
            content_type='application/json'
        )
        assert resp.status_code == 422

    def test_message_when_password_is_not_valid(self, client):
        resp = client.post(
            self.ENDPOINT,
            json=dict(
                full_name='bar',
                email='t@t.com',
                password='123',
                confirm_password='456',
                cpf_cnpj='11653754605',
                date_of_birth='2010-11-12'
            ),
            content_type='application/json'
        )
        response = resp.json
        assert response.get('errors').get('password')[0] == MSG_PASSWORD_DIDNT_MATCH

    def test_message_required_when_fullname_not_in_payload(self, client):
        resp = client.post(
            self.ENDPOINT,
            json=dict(email='teste@teste.com', password='123456', confirm_password='123456'),
            content_type='application/json'
        )
        print(resp.json)
        assert resp.json.get('errors').get('full_name')[0] == MSG_FIELD_REQUIRED

    def test_message_required_when_email_not_in_payload(self, client):
        resp = client.post(
            self.ENDPOINT,
            json=dict(full_name='teste', password='123456', confirm_password='123456'),
            content_type='application/json'
        )
        assert resp.json.get('errors').get('email')[0] == MSG_FIELD_REQUIRED

    @mock.patch("apps.users.repositories.User")
    def test_responses_already_exists(self, UserMock, client, mongo):
        UserMock.return_value.save.side_effect = NotUniqueError(
            "Some error occurred"
        )

        resp = client.post(
            self.ENDPOINT,
            json=dict(
                full_name='teste',
                email='teste@teste.com',
                password='123456',
                confirm_password='123456',
                cpf_cnpj='11653754605',
                date_of_birth='2010-11-12'
            ),
            content_type='application/json'
        )

        assert resp.status_code == 409
        assert resp.json.get('message') == MSG_ALREADY_EXISTS.format('usuário')

    def test_responses_ok(self, client, mongo):
        resp = client.post(
            self.ENDPOINT,
            json=dict(
                full_name='teste',
                email='teste@teste.com',
                password='123456',
                confirm_password='123456',
                cpf_cnpj='11653754605',
                date_of_birth='2010-11-12'
            ),
            content_type='application/json'
        )

        assert resp.status_code == 200
        assert resp.json.get('message') == MSG_RESOURCE_CREATED.format('Usuário')

    def test_responses_ok_with_cpf_masked(self, client, mongo):
        resp = client.post(
            self.ENDPOINT,
            json=dict(
                full_name='teste',
                email='teste@teste.com',
                password='123456',
                confirm_password='123456',
                cpf_cnpj='116.537.546-05',
                date_of_birth='2010-11-12'
            ),
            content_type='application/json'
        )

        assert resp.status_code == 200
        assert resp.json.get('message') == MSG_RESOURCE_CREATED.format('Usuário')
