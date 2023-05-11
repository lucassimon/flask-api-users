import pytest

from apps.users.utils import check_password_in_signup


@pytest.mark.parametrize("password,confirm_password,expected", [(None, 1, False), (1, None, False), (1,2,False), (2,2,True)])
def test_password(password, confirm_password, expected):
    assert check_password_in_signup(password, confirm_password) is expected
