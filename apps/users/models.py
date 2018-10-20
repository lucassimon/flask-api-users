# -*- coding: utf-8 -*-
# Python
from datetime import datetime

# Third
from mongoengine import (
    BooleanField,
    DateTimeField,
    EmailField,
    EmbeddedDocument,
    EmbeddedDocumentField,
    StringField,
)

# Apps
from apps.db import db


class Address(EmbeddedDocument):
    """
    Default implementation for address fields
    """
    meta = {
        'ordering': ['zip_code']
    }
    zip_code = StringField(default='')
    address = StringField(default='')
    number = StringField(default='')
    complement = StringField(default='')
    neighborhood = StringField(default='')
    city = StringField(default='')
    city_id = StringField(default='')
    state = StringField(default='')
    country = StringField(default='BRA')


class Roles(EmbeddedDocument):
    """
    Roles permissions
    """
    admin = BooleanField(default=False)


class UserMixin(db.Document):
    """
    Default implementation for User fields
    """
    meta = {
        'abstract': True,
        'ordering': ['email']
    }

    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    roles = EmbeddedDocumentField(Roles, default=Roles)
    created = DateTimeField(default=datetime.now)
    active = BooleanField(default=False)

    def is_active(self):
        return self.active

    def is_admin(self):
        return self.roles.admin


class User(UserMixin):
    '''
    Users are Buyers
    '''
    meta = {'collection': 'users'}

    full_name = StringField(required=True)
    cpf_cnpj = StringField(default='')
    address = EmbeddedDocumentField(Address, default=Address)
