# Third

from mongoengine import (
    BooleanField,
    StringField,
)

# Apps

from apps.users.models import User, Address

class TestAddress:

    def setup_method(self):
        self.address = {
            'zip_code': '31000-000', 'address': 'teste',
            'number': '12a', 'complement': 'teste', 'neighborhood': 'teste',
            'city': 'teste', 'state': 'teste', 'country': 'teste',
        }
        # Crio uma instancia do modelo User
        self.model = Address(**self.address)

    def test_zip_code_field_exists(self):
        """
        Verifico se o campo zip_code existe
        """
        assert 'zip_code' in self.model._fields

    def test_zip_code_field_is_required(self):
        """
        Verifico se o campo zip_code é requirido
        """
        assert self.model._fields['zip_code'].required is False

    def test_zip_code_field_is_unique(self):
        """
        Verifico se o campo zip_code é unico
        """
        assert self.model._fields['zip_code'].unique is False

    def test_zip_code_field_is_str(self):
        """
        Verifico se o campo zip_code é do tipo string
        """
        assert isinstance(self.model._fields['zip_code'], StringField)

    def test_zip_code_field_is_default_true(self):
        assert self.model._fields['zip_code'].default == ''

    def test_address_field_exists(self):
        """
        Verifico se o campo address existe
        """
        assert 'address' in self.model._fields

    def test_address_field_is_required(self):
        """
        Verifico se o campo address é requirido
        """
        assert self.model._fields['address'].required is False

    def test_address_field_is_unique(self):
        """
        Verifico se o campo address é unico
        """
        assert self.model._fields['address'].unique is False

    def test_address_field_is_str(self):
        """
        Verifico se o campo address é do tipo string
        """
        assert isinstance(self.model._fields['address'], StringField)

    def test_address_field_is_default_true(self):
        assert self.model._fields['address'].default == ''

    def test_number_field_exists(self):
        """
        Verifico se o campo number existe
        """
        assert 'number' in self.model._fields

    def test_number_field_is_required(self):
        """
        Verifico se o campo number é requirido
        """
        assert self.model._fields['number'].required is False

    def test_number_field_is_unique(self):
        """
        Verifico se o campo number é unico
        """
        assert self.model._fields['number'].unique is False

    def test_number_field_is_str(self):
        """
        Verifico se o campo number é do tipo string
        """
        assert isinstance(self.model._fields['number'], StringField)

    def test_number_field_is_default_true(self):
        assert self.model._fields['number'].default == ''

    def test_complement_field_exists(self):
        """
        Verifico se o campo complement existe
        """
        assert 'complement' in self.model._fields

    def test_complement_field_is_required(self):
        """
        Verifico se o campo complement é requirido
        """
        assert self.model._fields['complement'].required is False

    def test_complement_field_is_unique(self):
        """
        Verifico se o campo complement é unico
        """
        assert self.model._fields['complement'].unique is False

    def test_complement_field_is_str(self):
        """
        Verifico se o campo complement é do tipo string
        """
        assert isinstance(self.model._fields['complement'], StringField)

    def test_complement_field_is_default_true(self):
        assert self.model._fields['complement'].default == ''

    def test_neighborhood_field_exists(self):
        """
        Verifico se o campo neighborhood existe
        """
        assert 'neighborhood' in self.model._fields

    def test_neighborhood_field_is_required(self):
        """
        Verifico se o campo neighborhood é requirido
        """
        assert self.model._fields['neighborhood'].required is False

    def test_neighborhood_field_is_unique(self):
        """
        Verifico se o campo neighborhood é unico
        """
        assert self.model._fields['neighborhood'].unique is False

    def test_neighborhood_field_is_str(self):
        """
        Verifico se o campo neighborhood é do tipo string
        """
        assert isinstance(self.model._fields['neighborhood'], StringField)

    def test_neighborhood_field_is_default_true(self):
        assert self.model._fields['neighborhood'].default == ''

    def test_city_field_exists(self):
        """
        Verifico se o campo city existe
        """
        assert 'city' in self.model._fields

    def test_city_field_is_required(self):
        """
        Verifico se o campo city é requirido
        """
        assert self.model._fields['city'].required is False

    def test_city_field_is_unique(self):
        """
        Verifico se o campo city é unico
        """
        assert self.model._fields['city'].unique is False

    def test_city_field_is_str(self):
        """
        Verifico se o campo city é do tipo string
        """
        assert isinstance(self.model._fields['city'], StringField)

    def test_city_field_is_default_true(self):
        assert self.model._fields['city'].default == ''

    def test_city_id_field_exists(self):
        """
        Verifico se o campo city_id existe
        """
        assert 'city_id' in self.model._fields

    def test_city_id_field_is_required(self):
        """
        Verifico se o campo city_id é requirido
        """
        assert self.model._fields['city_id'].required is False

    def test_city_id_field_is_unique(self):
        """
        Verifico se o campo city_id é unico
        """
        assert self.model._fields['city_id'].unique is False

    def test_city_id_field_is_str(self):
        """
        Verifico se o campo city_id é do tipo string
        """
        assert isinstance(self.model._fields['city_id'], StringField)

    def test_city_id_field_is_default_true(self):
        assert self.model._fields['city_id'].default == ''

    def test_state_field_exists(self):
        """
        Verifico se o campo state existe
        """
        assert 'state' in self.model._fields

    def test_state_field_is_required(self):
        """
        Verifico se o campo state é requirido
        """
        assert self.model._fields['state'].required is False

    def test_state_field_is_unique(self):
        """
        Verifico se o campo state é unico
        """
        assert self.model._fields['state'].unique is False

    def test_state_field_is_str(self):
        """
        Verifico se o campo state é do tipo string
        """
        assert isinstance(self.model._fields['state'], StringField)

    def test_state_field_is_default_true(self):
        assert self.model._fields['state'].default == ''

    def test_country_field_exists(self):
        """
        Verifico se o campo country existe
        """
        assert 'country' in self.model._fields

    def test_country_field_is_required(self):
        """
        Verifico se o campo country é requirido
        """
        assert self.model._fields['country'].required is False

    def test_country_field_is_unique(self):
        """
        Verifico se o campo country é unico
        """
        assert self.model._fields['country'].unique is False

    def test_country_field_is_str(self):
        """
        Verifico se o campo country é do tipo string
        """
        assert isinstance(self.model._fields['country'], StringField)

    def test_country_field_is_default_true(self):
        assert self.model._fields['country'].default == 'BRA'


class TestUser:

    def setup_method(self):

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

    def test_is_active_is_false(self):
        assert self.model.is_active() is True

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

    def test_full_name_field_is_required(self):
        """
        Verifico se o campo full_name é requirido
        """
        assert self.model._fields['full_name'].required is True

    def test_cpf_cnpj_field_exists(self):
        """
        Verifico se o campo cpf_cnpj existe
        """
        assert 'cpf_cnpj' in self.model._fields

    def test_cpf_cnpj_field_is_required(self):
        """
        Verifico se o campo cpf_cnpj é requirido
        """
        assert self.model._fields['cpf_cnpj'].required is False

    def test_cpf_cnpj_field_is_unique(self):
        """
        Verifico se o campo cpf_cnpj é unico
        """
        assert self.model._fields['cpf_cnpj'].unique is False

    def test_cpf_cnpj_field_is_str(self):
        """
        Verifico se o campo cpf_cnpj é do tipo string
        """
        assert isinstance(self.model._fields['cpf_cnpj'], StringField)

    def test_cpf_cnpj_field_is_default_true(self):
        assert self.model._fields['cpf_cnpj'].default == ''

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
