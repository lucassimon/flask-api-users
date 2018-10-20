# -*- coding: utf-8 -*-

from apps.users.utils import check_password_in_signup


def test_password_none():
    assert check_password_in_signup(None, 1) is False


def test_confirm_password_none():
    assert check_password_in_signup(1, None) is False


def test_password_confirm_password_are_differents():
    assert check_password_in_signup(1, 2) is False


def test_password_confirm_password_are_equal():
    assert check_password_in_signup(2, 2) is True
