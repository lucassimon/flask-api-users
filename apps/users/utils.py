# -*- coding: utf-8


def check_password_in_signup(password, confirm_password):

    if not password:
        return False

    if not confirm_password:
        return False

    if not password == confirm_password:
        return False

    return True
