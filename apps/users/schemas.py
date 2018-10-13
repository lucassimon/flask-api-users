# -*- coding: utf-8 -*-


from marshmallow import Schema
from marshmallow.fields import Email, Str, Boolean

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
