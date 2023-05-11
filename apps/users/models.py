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
import mongoengine as me
# Apps
from apps.extensions.db import db


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
    superuser = BooleanField(default=True)
    manager = BooleanField(default=False)
    coordinators = BooleanField(default=False)
    vendors = BooleanField(default=False)


class UserMixin(me.Document):
    """
    Default implementation for User fields
    """
    meta = {
        'abstract': True,
        'ordering': ['email']
    }

    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    created = DateTimeField(default=datetime.now)
    active = BooleanField(default=True)

    def is_active(self):
        return self.active


class User(UserMixin):
    '''
    Users
    '''
    meta = {'collection': 'users'}

    full_name = StringField(required=True)
    cpf_cnpj = StringField(required=True, unique=True)
    date_of_birth = DateTimeField(required=True)
    address = EmbeddedDocumentField(Address, default=Address)


class Admin(UserMixin):
    '''
    Admin users
    '''
    meta = {'collection': 'admins'}

    full_name = StringField(required=True)
    roles = EmbeddedDocumentField(Roles, default=Roles)
