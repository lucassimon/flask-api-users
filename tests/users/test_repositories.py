import pytest
from unittest import mock

from mongoengine.errors import NotUniqueError, ValidationError, FieldDoesNotExist, DoesNotExist, MultipleObjectsReturned

from apps.users.repositories import AdminMongoRepository, UserMongoRepository
from apps.users.models import User, Admin
from apps.users.exceptions import UserMongoNotUniqueException, UserMongoValidationErrorException, UserMongoFieldsDoesNotExistException, UserMongoDoesNotExistException
from tests.factories.users import AdminFactory, UserFactory


class TestUserRepoInsert:
    def setup_method(self):
        UserFactory.reset_sequence()

    def teardown_method(self):
        User.objects.delete()

    @mock.patch("apps.users.repositories.User.save", side_effect=NotUniqueError)
    def test_should_raises_not_unique_exception(self, client, mongo):
        with pytest.raises(UserMongoNotUniqueException) as exc:
            UserMongoRepository().insert(data={
                'full_name': 'some-full-name',
                'email': 'some-email',
                'cpf_cnpj': 'some-cpf',
                'date_of_birth': 'some-date',
                'password': 'some-password'
            })

    @mock.patch("apps.users.repositories.User.save", side_effect=ValidationError)
    def test_should_raises_validation_exception(self, client, mongo):
        with pytest.raises(UserMongoValidationErrorException) as exc:
            UserMongoRepository().insert(data={
                'full_name': 'some-full-name',
                'email': 'some-email',
                'cpf_cnpj': 'some-cpf',
                'date_of_birth': 'some-date',
                'password': 'some-password'
            })

    @mock.patch("apps.users.repositories.User.save", side_effect=Exception)
    def test_should_raises_exception(self, client, mongo):
        with pytest.raises(Exception) as exc:
            UserMongoRepository().insert(data={
                'full_name': 'some-full-name',
                'email': 'some-email',
                'cpf_cnpj': 'some-cpf',
                'date_of_birth': 'some-date',
                'password': 'some-password'
            })

    @mock.patch("apps.users.repositories.User.save")
    def test_should_return_user_instance(self, SaveMock, client, mongo):
        model = UserMongoRepository().insert(data={
            'full_name': 'some-full-name',
            'email': 'some-email',
            'cpf_cnpj': 'some-cpf',
            'date_of_birth': 'some-date',
            'password': 'some-password'
        })

        assert model.email == 'some-email'
        assert isinstance(model, User) is True


class TestAdminRepoInsert:
    def setup_method(self):
        AdminFactory.reset_sequence()

    def teardown_method(self):
        Admin.objects.delete()

    @mock.patch("apps.users.repositories.Admin.save", side_effect=NotUniqueError)
    def test_should_raises_not_unique_exception(self, client, mongo):
        with pytest.raises(UserMongoNotUniqueException) as exc:
            AdminMongoRepository().insert(data={
                'full_name': 'some-full-name',
                'email': 'some-email',
                'password': 'some-password'
            })

    @mock.patch("apps.users.repositories.Admin.save", side_effect=ValidationError)
    def test_should_raises_validation_exception(self, client, mongo):
        with pytest.raises(UserMongoValidationErrorException) as exc:
            AdminMongoRepository().insert(data={
                'full_name': 'some-full-name',
                'email': 'some-email',
                'password': 'some-password'
            })

    @mock.patch("apps.users.repositories.Admin.save", side_effect=Exception)
    def test_should_raises_exception(self, client, mongo):
        with pytest.raises(Exception) as exc:
            AdminMongoRepository().insert(data={
                'full_name': 'some-full-name',
                'email': 'some-email',
                'password': 'some-password'
            })

    @mock.patch("apps.users.repositories.Admin.save")
    def test_should_return_user_instance(self, SaveMock, client, mongo):
        model = AdminMongoRepository().insert(data={
            'full_name': 'Admin',
            'email': 'some-email@admin.com',
            'password': 'some-password'
        })

        assert model.email == 'some-email@admin.com'
        assert isinstance(model, Admin) is True


class TestAdminRepoGetUserByCpf:
    def setup_method(self):
        AdminFactory.reset_sequence()
        UserFactory.reset_sequence()

    def teardown_method(self):
        Admin.objects.delete()
        User.objects.delete()

    # @mock.patch("apps.users.repositories.User.objects")
    def test_should_return_an_user(self, client, mongo):
        user = UserFactory.create()
        # GetMock.get.return_value = user
        model = AdminMongoRepository().get_user_by_cpf_cnpj(user.cpf_cnpj)
        assert model.cpf_cnpj == user.cpf_cnpj

    @mock.patch("apps.users.repositories.User.objects.get", side_effect=DoesNotExist)
    def test_should_raises_does_not_exist(self, GetMock, client, mongo):
        with pytest.raises(UserMongoDoesNotExistException) as exc:
            AdminMongoRepository().get_user_by_cpf_cnpj('some-cpf')

    @mock.patch("apps.users.repositories.User.objects")
    def test_should_raises_field_does_not_exist(self, ObjectsMock, client, mongo):
        ObjectsMock.get.side_effect = FieldDoesNotExist()
        with pytest.raises(UserMongoFieldsDoesNotExistException) as exc:
            AdminMongoRepository().get_user_by_cpf_cnpj('some-cpf')

    @mock.patch("apps.users.repositories.User.objects")
    def test_should_raises_exception(self, GetMock, client, mongo):
        GetMock.get.side_effect = Exception()
        with pytest.raises(Exception) as exc:
            AdminMongoRepository().get_user_by_cpf_cnpj('some-cpf')
