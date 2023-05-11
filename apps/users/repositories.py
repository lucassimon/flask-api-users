from mongoengine.errors import NotUniqueError, ValidationError, FieldDoesNotExist, DoesNotExist, MultipleObjectsReturned

from .models import User, Admin
from .exceptions import (
    UserMongoNotUniqueException, UserMongoValidationErrorException, UserMongoDoesNotExistException,
    UserMongoFieldsDoesNotExistException, UserMongoMultipleObjectsReturnedException
)


class UserMongoRepository:

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


class AdminMongoRepository:
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

    def get_user_by_id(user_id: str):
        try:
            # buscamos todos os usuários da base utilizando o paginate
            return User.objects.get(id=user_id)

        except DoesNotExist:
            raise UserMongoDoesNotExistException from DoesNotExist

        except FieldDoesNotExist:
            raise UserMongoFieldsDoesNotExistException from FieldDoesNotExist

        except Exception as err:
            raise err

    def exists_email_in_users(email: str, instance=None):
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

