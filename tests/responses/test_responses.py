# -*- coding: utf-8 -*-
import pytest

from apps.extensions.responses import resp_data_invalid, resp_exception
from apps.extensions.responses import resp_does_not_exist, resp_already_exists, resp_ok

from apps.extensions.messages import MSG_INVALID_DATA, MSG_EXCEPTION, MSG_DOES_NOT_EXIST
from apps.extensions.messages import MSG_ALREADY_EXISTS


def test_resp_data_invalid_raises_error(client):
    with pytest.raises(ValueError):
        resp_data_invalid(None, {})


def test_resp_data_invalid_response_status_code_422(client):
    resp = resp_data_invalid('pytest', {})
    assert resp.status_code == 422


def test_resp_data_invalid_response(client):
    resp = resp_data_invalid('pytest', {})
    message = resp.json.get('message')
    assert message == MSG_INVALID_DATA


def test_resp_exception_raises_error(client):
    with pytest.raises(ValueError):
        resp_exception(None, {})


def test_resp_exception_response_status_code_500(client):
    resp = resp_exception('pytest', 'Exception raises')
    assert resp.status_code == 500


def test_resp_exception_response(client):
    resp = resp_exception('pytest', {})
    message = resp.json.get('message')
    assert message == MSG_EXCEPTION


def test_resp_does_not_exist_raises_error(client):
    with pytest.raises(ValueError):
        resp_does_not_exist(None, None)


def test_resp_does_not_exist_response_status_code_404(client):
    resp = resp_does_not_exist('pytest', 'Some description')
    assert resp.status_code == 404


def test_resp_does_not_exist_response(client):
    description = 'Some description'
    resp = resp_does_not_exist('pytest', description)
    message = resp.json.get('message')
    assert message == MSG_DOES_NOT_EXIST.format(description)


def test_resp_already_exists_raises_error(client):
    with pytest.raises(ValueError):
        resp_already_exists(None, None)


def test_resp_already_exists_response_status_code_400(client):
    resp = resp_already_exists('pytest', 'Some description')
    assert resp.status_code == 409


def test_resp_already_exists_response(client):
    description = 'Some description'
    resp = resp_already_exists('pytest', description)
    message = resp.json.get('message')
    assert message == MSG_ALREADY_EXISTS.format(description)


def test_resp_ok_response_status_code_200(client):
    resource = 'pytest'
    message = 'pytest retornado com sucesso'
    data = {'foo': 'bar'}
    extras = {'ping': 'pong'}
    resp = resp_ok(resource, message, data, **extras)
    assert resp.status_code == 200


def test_resp_ok_response_message(client):
    resource = 'pytest'
    message = 'pytest retornado com sucesso'
    data = {'foo': 'bar'}
    extras = {'ping': 'pong'}
    resp = resp_ok(resource, message, data, **extras)
    assert resp.json.get('message') == message


def test_resp_ok_response_data(client):
    resource = 'pytest'
    message = 'pytest retornado com sucesso'
    data = {'foo': 'bar'}
    extras = {'ping': 'pong'}
    resp = resp_ok(resource, message, data, **extras)
    assert resp.json.get('data').get('foo') == 'bar'


def test_resp_ok_response_extra(client):
    resource = 'pytest'
    message = 'pytest retornado com sucesso'
    data = {'foo': 'bar'}
    extras = {'ping': 'pong'}
    resp = resp_ok(resource, message, data, **extras)
    assert resp.json.get('ping') == 'pong'
