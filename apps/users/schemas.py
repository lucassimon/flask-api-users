# -*- coding: utf-8 -*-


from marshmallow import Schema
from marshmallow.fields import Email, Str, Boolean, Nested

from apps.messages import MSG_FIELD_REQUIRED


class UserRegistrationSchema(Schema):
    full_name = Str(
        required=True, error_messages={'required': MSG_FIELD_REQUIRED}
    )
    email = Email(
        required=True, error_messages={'required': MSG_FIELD_REQUIRED}
    )
    password = Str(
        required=True, error_messages={'required': MSG_FIELD_REQUIRED}
    )


class UserSchema(Schema):
    id = Str()
    full_name = Str(
        required=True, error_messages={'required': MSG_FIELD_REQUIRED}
    )
    email = Email(
        required=True, error_messages={'required': MSG_FIELD_REQUIRED}
    )
    cpf_cnpj = Str()
    active = Boolean()


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
    email = Email()
    cpf_cnpj = Str()
    address = Nested(AddressSchema)
