from marshmallow import Schema, pre_load, post_load, validates, validates_schema, ValidationError
from marshmallow.fields import Email, Str, Boolean, Nested, Date

from apps.extensions.messages import MSG_FIELD_REQUIRED

from .utils import Cpf, check_password_in_signup



def check_cpf(data):
    return Cpf(data).validate()


class RolesSchema(Schema):
    superuser = Boolean()
    manager = Boolean()
    coordinators = Boolean()
    vendors = Boolean()


class CreateAdminInput(Schema):
    full_name = Str(
        required=True, error_messages={'required': MSG_FIELD_REQUIRED}
    )
    email = Email(
        required=True, error_messages={'required': MSG_FIELD_REQUIRED}
    )
    password = Str(
        required=True, load_only=True,error_messages={'required': MSG_FIELD_REQUIRED}
    )

    roles = Nested(RolesSchema)

    @post_load
    def lower_email(self, payload, **kwargs):
        # transformo o email para lowercase e retiro espaços
        payload["email"] = payload["email"].lower().strip()
        return payload


class CreateUserInput(Schema):
    full_name = Str(
        required=True, error_messages={'required': MSG_FIELD_REQUIRED}
    )
    email = Email(
        required=True, error_messages={'required': MSG_FIELD_REQUIRED}
    )
    cpf_cnpj = Str(required=True, error_messages={'required': MSG_FIELD_REQUIRED})
    date_of_birth = Date(required=True, error_messages={'required': MSG_FIELD_REQUIRED})
    password = Str(
        required=True, load_only=True,error_messages={'required': MSG_FIELD_REQUIRED}
    )
    confirm_password = Str(
        required=True, load_only=True, error_messages={'required': MSG_FIELD_REQUIRED}
    )

    def normalize_cpf_cnpj(self, value, **kwargs):
        # normalizo a string retirando caracteres especiais
        cpf_instance = Cpf(value)
        return cpf_instance.cpf

    @post_load
    def lower_email(self, payload, **kwargs):
        # transformo o email para lowercase e retiro espaços
        payload["email"] = payload["email"].lower().strip()
        return payload

    @post_load
    def render_cpf_cnpj(self, payload, **kwargs):
        payload["cpf_cnpj"] = self.normalize_cpf_cnpj(payload["cpf_cnpj"])
        return payload

    @post_load
    def remove_confirm_password(self, payload, **kwargs):
        del payload["confirm_password"]
        return payload

    @validates_schema
    def validate_password(self, data, **kwargs):
        # verifico através de uma função a senha e a confirmação da senha
        # Se as senhas não são iguais retorno uma respota inválida
        if not check_password_in_signup(data['password'], data['confirm_password']):
            raise ValidationError("Password did not matches", "password")

    @validates("cpf_cnpj")
    def validate_cpf_cnpj(self, value):
        data = self.normalize_cpf_cnpj(value)
        if len(data) == 11:
            if not check_cpf(data):
                raise ValidationError("CPF is wrong.", field_name="cpf_cnpj")

        elif len(data) == 14:
            pass

        else:
            raise ValidationError("Field cpf_cnpj is wrong", field_name="cpf_cnpj")


class UserSchema(Schema):
    id = Str()
    full_name = Str(
        required=True, error_messages={'required': MSG_FIELD_REQUIRED}
    )
    email = Email(
        required=True, error_messages={'required': MSG_FIELD_REQUIRED}
    )
    cpf_cnpj = Str()
    date_of_birth = Date()
    active = Boolean()


class CreateUserOutput(UserSchema):
    pass


class AddressSchema(Schema):
    zip_code = Str()
    address = Str()
    number = Str()
    complement = Str()
    neighborhood = Str()
    city = Str()
    city_id = Str()
    state = Str()
    country = Str()


class UserUpdateSchema(Schema):
    full_name = Str()
    address = Nested(AddressSchema)



