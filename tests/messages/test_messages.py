# -*- coding: utf-8 -*-

from apps.messages import MSG_FIELD_REQUIRED, MSG_INVALID_DATA
from apps.messages import MSG_DOES_NOT_EXIST, MSG_EXCEPTION
from apps.messages import MSG_ALREADY_EXISTS, MSG_NO_DATA
from apps.messages import MSG_PASSWORD_DIDNT_MATCH, MSG_RESOURCE_CREATED


def test_msg_field_required():
    assert MSG_FIELD_REQUIRED == 'Campo obrigatório.'


def test_msg_invalid_data():
    assert MSG_INVALID_DATA == 'Ocorreu um erro nos campos informados.'


def test_msg_does_not_exist():
    assert MSG_DOES_NOT_EXIST == 'Este(a) {} não existe.'


def test_msg_exception():
    msg = 'Ocorreu um erro no servidor. Contate o administrador.'
    assert MSG_EXCEPTION == msg


def test_msg_already_exists():
    assert MSG_ALREADY_EXISTS == 'Já existe um(a) {} com estes dados.'


def test_msg_no_data():
    assert MSG_NO_DATA == 'Nenhum dado foi postado.'


def test_msg_password_wrong():
    assert MSG_PASSWORD_DIDNT_MATCH == 'As senhas não conferem.'


def test_msg_resource_created():
    assert MSG_RESOURCE_CREATED == '{} criado(a).'
