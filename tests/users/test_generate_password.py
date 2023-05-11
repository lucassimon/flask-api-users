import pytest
from unittest import mock

from apps.users.utils import generate_password


def test_should_return_password_encrypted():
    with mock.patch("apps.users.utils.hashpw") as haspw_mock:
        haspw_mock.return_value = b"$2b$12$encyptPassword"
        received = generate_password("132456")

        assert received == b"$2b$12$encyptPassword"
