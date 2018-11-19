# -*- coding: utf-8

# Third

from mongoengine.errors import FieldDoesNotExist, DoesNotExist, MultipleObjectsReturned

# Apps
from apps.responses import resp_exception, resp_does_not_exist

# Local
from .models import User


def check_password_in_signup(password: str, confirm_password: str):

    if not password:
        return False

    if not confirm_password:
        return False

    if not password == confirm_password:
        return False

    return True


def get_user_by_id(user_id: str):
    try:
        # buscamos todos os usuários da base utilizando o paginate
        return User.objects.get(id=user_id)

    except DoesNotExist:
        return resp_does_not_exist('Users', 'Usuário')

    except FieldDoesNotExist as e:
        return resp_exception('Users', description=e.__str__())

    except Exception as e:
        return resp_exception('Users', description=e.__str__())


def exists_email_in_users(email: str, instance=None):
    """
    Verifico se existe um usuário com aquele email
    """
    user = None

    try:
        user = User.objects.get(email=email)

    except DoesNotExist:
        return False

    except MultipleObjectsReturned:
        return True

    # verifico se o id retornado na pesquisa é mesmo da minha instancia
    # informado no parâmetro
    if instance and instance.id == user.id:
        return False

    return True


def get_user_by_email(email: str):
    try:
        # buscamos todos os usuários da base utilizando o paginate
        return User.objects.get(email=email)

    except DoesNotExist:
        return resp_does_not_exist('Users', 'Usuário')

    except FieldDoesNotExist as e:
        return resp_exception('Users', description=e.__str__())

    except Exception as e:
        return resp_exception('Users', description=e.__str__())
