from mongoengine.errors import NotUniqueError, ValidationError, FieldDoesNotExist, DoesNotExist, MultipleObjectsReturned
from flask_mongoengine import Pagination
from .models import User, Admin
from .exceptions import (
    UserMongoNotUniqueException, UserMongoValidationErrorException, UserMongoDoesNotExistException,
    UserMongoFieldsDoesNotExistException, UserMongoMultipleObjectsReturnedException
)

class UserMongoMixin:
    def get_user_by_email(self, email: str):
        try:
            # buscamos todos os usuários da base utilizando o paginate
            return User.objects.get(email=email)

        except DoesNotExist:
            raise UserMongoDoesNotExistException from DoesNotExist

        except FieldDoesNotExist:
            raise UserMongoFieldsDoesNotExistException from FieldDoesNotExist

        except Exception as err:
            raise err


class UserMongoRepository(UserMongoMixin):
    def insert(self, data) -> None:
        try:
            model = User(**data)
            model.save()
            return model
        except NotUniqueError as err:
            raise UserMongoNotUniqueException from err

        except ValidationError as err:
            raise UserMongoValidationErrorException from err

        except Exception as err:
            raise err


class AdminMongoRepository(UserMongoMixin):
    def insert(self, data) -> None:
        try:
            model = Admin(**data).save()
            return model
        except NotUniqueError as err:
            raise UserMongoNotUniqueException from err

        except ValidationError as err:
            raise UserMongoValidationErrorException from err

        except Exception as err:
            raise err

    def get_admin_by_email(self, email: str):
        try:
            # buscamos todos os usuários da base utilizando o paginate
            return Admin.objects.get(email=email)

        except DoesNotExist:
            raise UserMongoDoesNotExistException from DoesNotExist

        except FieldDoesNotExist:
            raise UserMongoFieldsDoesNotExistException from FieldDoesNotExist

        except Exception as err:
            raise err

    def get_users_with_pagination(self, page_id=1, page_size=10):
        try:
            # buscamos todos os usuarios da base utilizando o paginate
            users = User.objects()
            return Pagination(iterable=users, page=page_id, per_page=page_size)

        except FieldDoesNotExist:
            raise UserMongoFieldsDoesNotExistException from FieldDoesNotExist

        except Exception as err:
            raise err

    def get_user_by_id(self, user_id: str):
        try:
            # buscamos todos os usuários da base utilizando o paginate
            return User.objects.get(id=user_id)

        except DoesNotExist:
            raise UserMongoDoesNotExistException from DoesNotExist

        except FieldDoesNotExist:
            raise UserMongoFieldsDoesNotExistException from FieldDoesNotExist

        except Exception as err:
            raise err

    def get_user_by_cpf_cnpj(self, cpf_cnpj: str):
        try:
            # buscamos todos os usuários da base utilizando o paginate
            return User.objects.get(cpf_cnpj=cpf_cnpj)

        except DoesNotExist:
            raise UserMongoDoesNotExistException from DoesNotExist

        except FieldDoesNotExist:
            raise UserMongoFieldsDoesNotExistException from FieldDoesNotExist

        except Exception as err:
            raise err

    def exists_email_in_users(self, email: str, instance=None):
        """
        Verifico se existe um usuário com aquele email
        """
        user = None

        try:
            user = User.objects.get(email=email)

        except DoesNotExist:
            raise UserMongoDoesNotExistException from DoesNotExist

        except MultipleObjectsReturned:
            raise UserMongoMultipleObjectsReturnedException from MultipleObjectsReturned

        # verifico se o id retornado na pesquisa é mesmo da minha instancia
        # informado no parâmetro
        if instance and instance.id == user.id:
            return False

        return True

    def update_user(self, user, data):
        try:
            # para cada chave dentro do dados do update schema
            # atribuimos seu valor
            for i in data.keys():
                user[i] = data[i]

            user.save()

        except NotUniqueError as err:
            raise UserMongoNotUniqueException from err

        except ValidationError as err:
            raise UserMongoValidationErrorException from err

        except Exception as err:
            raise err

    def delete_user(self, user):
        try:
            user.active = False
            user.save()

        except NotUniqueError as err:
            raise UserMongoNotUniqueException from err

        except ValidationError as err:
            raise UserMongoValidationErrorException from err


        except Exception as err:
            raise err
