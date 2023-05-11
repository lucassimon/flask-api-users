import pytest

from apps.users.utils import Cpf


def test_cpf_when_length_is_less_than_11():
    is_valid = Cpf('123456').validate()
    assert is_valid is False

@pytest.mark.parametrize("rest,expected", [(1, 0), (8, 3)])
def test_cpf_rule(rest,expected):
    value = Cpf('123456').cpf_rule(rest)
    assert value == expected

@pytest.mark.parametrize("cpf,expected", [(92144721068, 6), ('92144721068', 6), ('921.447.210-68', 6)])
def test_cpf_first_digit(cpf, expected):
    first_digit = Cpf(cpf).calculate_first_digit()
    assert first_digit == expected

@pytest.mark.parametrize("cpf,expected", [(92144721068, 8), ('92144721068', 8), ('921.447.210-68', 8)])
def test_cpf_second_digit(cpf, expected):
    second_digit = Cpf(cpf).calculate_second_digit()
    assert second_digit == expected

@pytest.mark.parametrize("cpf,expected", [(92144721068, True), ('92144721068', True), ('921.447.210-68', True)])
def test_cpf_is_valid(cpf, expected):
    is_valid = Cpf(cpf).validate()
    assert is_valid is expected

def test_cpf_normalize():
    cpf = Cpf('921.447.210-68')
    assert cpf.cpf == '92144721068'

def test_cpf_as_numbers_only():
    cpf = Cpf('92144721068')
    assert cpf.cpf == '92144721068'
