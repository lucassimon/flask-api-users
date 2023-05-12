from unittest import mock

from apps.auth.exceptions import LoginSchemaValidationErrorException
from apps.users.exceptions import UserMongoDoesNotExistException


class TestAuthUser:

    @mock.patch("apps.auth.resources.AuthUsersCommand.run")
    def test_responses_data_invalid(self, AuthUsersCommandMock, client, mongo):
        AuthUsersCommandMock.side_effect = LoginSchemaValidationErrorException(
            "Some error occurred"
        )

        resp = client.post(
            '/auth',
            json=dict(
                email='teste@teste.com',
                password='123456',
            ),
            content_type='application/json'
        )

        assert resp.status_code == 422
        assert resp.json.get('message') == 'The input data is wrong'
        assert resp.json.get('errors') == 'Some error occurred'

    @mock.patch("apps.auth.resources.AuthUsersCommand.run")
    def test_responses_user_does_not_exist(self, AuthUsersCommandMock, client, mongo):
        AuthUsersCommandMock.side_effect = UserMongoDoesNotExistException(
            "Some error occurred"
        )

        resp = client.post(
            '/auth',
            json=dict(
                email='teste@teste.com',
                password='123456',
            ),
            content_type='application/json'
        )

        assert resp.status_code == 404
        assert resp.json.get('message') == 'Este(a) usuário não existe.'

    @mock.patch("apps.auth.resources.AuthUsersCommand.run")
    def test_responses_user_exception(self, AuthUsersCommandMock, client, mongo):
        AuthUsersCommandMock.side_effect = Exception(
            "Some error occurred"
        )

        resp = client.post(
            '/auth',
            json=dict(
                email='teste@teste.com',
                password='123456',
            ),
            content_type='application/json'
        )

        assert resp.status_code == 500
        assert resp.json.get('message') == 'Some error occurred'
