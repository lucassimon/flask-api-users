from unittest import mock

from apps.auth.exceptions import LoginSchemaValidationErrorException
from apps.users.exceptions import UserMongoDoesNotExistException


class TestAdminUserResourceByCpf:
    @mock.patch("apps.users.resources_admin.GetUserByCpfCnpjCommand.run")
    def test_responses_user_does_not_exist(self, GetUserByCpfCnpjCommandMock, client, auth, mongo):
        GetUserByCpfCnpjCommandMock.side_effect = UserMongoDoesNotExistException(
            "Some error occurred"
        )

        headers = {"Authorization": f"Bearer {client.access_token}"}
        url = '/admin/users/cpf/{}'.format('some-cpf')
        resp = client.get(url, content_type='application/json', headers=headers)

        assert resp.status_code == 404
        assert resp.json.get('message') == 'Este(a) usuário não existe.'

    @mock.patch("apps.users.resources_admin.GetUserByCpfCnpjCommand.run")
    def test_responses_user_exception(self, GetUserByCpfCnpjCommandMock, client, auth, mongo):
        GetUserByCpfCnpjCommandMock.side_effect = Exception(
            "Some error occurred"
        )

        headers = {"Authorization": f"Bearer {client.access_token}"}
        url = '/admin/users/cpf/{}'.format('some-cpf')
        resp = client.get(url, content_type='application/json', headers=headers)

        assert resp.status_code == 500
        assert resp.json.get('message') == 'Some error occurred'
