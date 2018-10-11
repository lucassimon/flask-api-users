# -*- coding: utf-8 -*-
import pytest

from json import dumps, loads

from apps.messages import MSG_NO_DATA, MSG_INVALID_DATA, MSG_PASSWORD_DIDNT_MATCH
from apps.messages import MSG_FIELD_REQUIRED, MSG_RESOURCE_CREATED, MSG_ALREADY_EXISTS
from apps.responses import resp_data_invalid


class TestSignUp:

    def setup_method(self):
        self.data = {}
        self.ENDPOINT = '/users'

    def test_response_422_when_empty_payload(self, client):
        resp = client.post(self.ENDPOINT)
        assert resp.status_code == 422

    def test_message_when_empty_payload(self, client):
        resp = client.post(self.ENDPOINT)
        assert resp.json.get('message') == MSG_NO_DATA

    def test_response_422_when_data_is_not_valid(self, client):
        resp = client.post(
            self.ENDPOINT,
            data=dumps(dict(foo='bar')),
            content_type='application/json'
        )
        assert resp.status_code == 422

    def test_message_when_password_is_not_valid(self, client):
        resp = client.post(
            self.ENDPOINT,
            data=dumps(dict(foo='bar')),
            content_type='application/json'
        )
        assert resp.json.get('message') == MSG_INVALID_DATA
        assert resp.json.get('errors').get('password') == MSG_PASSWORD_DIDNT_MATCH

    def test_message_required_when_fullname_not_in_payload(self, client):
        resp = client.post(
            self.ENDPOINT,
            data=dumps(dict(email='teste@teste.com', password='123456', confirm_password='123456')),
            content_type='application/json'
        )
        assert resp.json.get('message') == MSG_INVALID_DATA
        assert resp.json.get('errors').get('full_name')[0] == MSG_FIELD_REQUIRED

    def test_message_required_when_email_not_in_payload(self, client):
        resp = client.post(
            self.ENDPOINT,
            data=dumps(dict(full_name='teste', password='123456', confirm_password='123456')),
            content_type='application/json'
        )
        assert resp.json.get('message') == MSG_INVALID_DATA
        assert resp.json.get('errors').get('email')[0] == MSG_FIELD_REQUIRED

    def test_responses_already_exists(self, client, mongo):
        client.post(
            self.ENDPOINT,
            data=dumps(dict(full_name='teste', email='teste@teste.com', password='123456', confirm_password='123456')),
            content_type='application/json'
        )

        resp_2 = client.post(
            self.ENDPOINT,
            data=dumps(dict(full_name='teste', email='teste@teste.com', password='123456', confirm_password='123456')),
            content_type='application/json'
        )

        assert resp_2.status_code == 400
        assert resp_2.json.get('message') == MSG_ALREADY_EXISTS.format('usuário')


    def test_responses_ok(self, client, mongo):
        resp = client.post(
            self.ENDPOINT,
            data=dumps(dict(full_name='teste', email='teste@teste.com', password='123456', confirm_password='123456')),
            content_type='application/json'
        )

        assert resp.status_code == 200
        assert resp.json.get('message') == MSG_RESOURCE_CREATED.format('Usuário')
