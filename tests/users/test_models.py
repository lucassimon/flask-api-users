# Third

from mongoengine import (
    BooleanField,
    StringField,
)

# Apps

from apps.users.models import User


class TestUser:

    def setup_method(self):
        self.address = {
            'zip_code': '31000-000', 'address': 'teste',
            'number': '12a', 'info': 'teste', 'neighborhood': 'teste',
            'city': 'teste', 'state': 'teste', 'country': 'teste',
        }
        self.data = {
            'email': 'teste1@teste.com', 'password': 'teste123',
            'active': True, 'full_name': 'Teste',
            'cpf_cnpj': '11111111111'
        }

        # Crio uma instancia do modelo User
        self.model = User(**self.data)

    def test_email_field_exists(self):
        """
        Verifico se o campo email existe
        """
        assert 'email' in self.model._fields

    def test_email_field_is_required(self):
        """
        Verifico se o campo email é requirido
        """
        assert self.model._fields['email'].required is True

    def test_email_field_is_unique(self):
        """
        Verifico se o campo email é unico
        """
        assert self.model._fields['email'].unique is True

    def test_email_field_is_str(self):
        """
        Verifico se o campo email é do tipo string
        """
        assert isinstance(self.model._fields['email'], StringField)

    def test_active_field_exists(self):
        assert 'active' in self.model._fields

    def test_active_field_is_default_true(self):
        assert self.model._fields['active'].default is False

    def test_active_field_is_bool(self):
        """
        Verifico se o campo active é booleano
        """
        assert isinstance(self.model._fields['active'], BooleanField)

    def test_full_name_field_exists(self):
        """
        Verifico se o campo full_name existe
        """
        assert 'full_name' in self.model._fields

    def test_full_name_field_is_str(self):
        assert isinstance(self.model._fields['full_name'], StringField)

    def test_all_fields_in_model(self):
        """
        Verifico se todos os campos estão de fato no meu modelo
        """
        fields = [
            'active', 'address', 'cpf_cnpj', 'created', 'email',
            'full_name', 'id', 'password', 'roles'
        ]

        model_keys = [i for i in self.model._fields.keys()]

        fields.sort()
        model_keys.sort()

        assert fields == model_keys
