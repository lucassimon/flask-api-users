# -*- coding: utf-8 -*-

# Python
from os.path import dirname, isfile, join

import pytest
from dotenv import load_dotenv

# a partir do arquivo atual adicione ao path o arquivo .env
_ENV_FILE = join(dirname(__file__), '../.env')

# existindo o arquivo faça a leitura do arquivo através da função load_dotenv
if isfile(_ENV_FILE):
    load_dotenv(dotenv_path=_ENV_FILE)

# Cria uma fixture que será utilizada no escopo sessão
# ou seja a cada execução do comando pytest


@pytest.fixture(scope='session')
def client():
    from apps.app import create_app
    # instancia nossa função factory criada anteriormente
    flask_app = create_app(testing=True)

    # O Flask fornece um caminho para testar a aplicação
    # utilizando o Werkzeug test Client
    # e manipulando o contexto (configurações)
    testing_client = flask_app.test_client()

    # Antes de executar os testes, é criado um contexto com as configurações
    # da aplicação
    ctx = flask_app.app_context()
    ctx.push()

    # retorna o client criado
    yield testing_client  # this is where the testing happens!

    # remove o contexto ao terminar os testes
    ctx.pop()


@pytest.fixture(scope='function')
def mongo(request, client):

    from apps.extensions.db import db

    yield db

    def fin(db):
        print("\n[teardown] disconnect from db")

    db.connection.drop_database("api-users-test")
    db.connection.close()
    fin(db)


@pytest.fixture(scope="session")
def auth(client):
    from tests.factories.users import AdminFactory
    from flask_jwt_extended import create_access_token, create_refresh_token
    from apps.users.utils import generate_password

    admin = AdminFactory.create(
        id="5ce089d4fb5d1b3bd3ad96a2",
        name="Admin",
        email="supertest@mail.com",
        password=generate_password("123456"),
    )
    access_token = create_access_token(
        identity=admin.email, expires_delta=False, fresh=True
    )
    refresh_token = create_refresh_token(identity=admin.email, expires_delta=False)
    client.access_token = access_token
    client.refresh_token = refresh_token
    client.user_id = f"{admin.id}"
    return client
