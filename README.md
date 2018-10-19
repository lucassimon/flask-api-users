# flask-api-users

Uma api com Flask Framework, MongoDB e autenticação JWT

![coverage](./static/coverage.svg)

## Commands

```shell
make clean:
       Removes all pyc, pyo and __pycache__

make clean-build:
       Clear all build directories

make setup_dev
       Install dev dependencies and flake8 webhook
       Needs virtualenv activated and git initalized

make setup
       Install prod dependencies
       Needs virtualenv activated and git initalized

make isort:
       Run isort command cli in development features

make lint:
       Run lint

make coverage:
       Run tests with coverage and generate a badge (svg)

make test:
       Run tests with coverage, lint, and clean commands

make dev:
       Run the dev web application, with tests and coverage

make run:
       Run the web application without tests

make release:
       Creates a new tag and set the version in this package
       Ex: make release v=1.0.0
```
## Inicio

Execute o `make setup_dev` com o virtualenv ativo e o git inicializado, para fazer o setup inicial da aplicação instalando as dependências de desenvolvimento.

Caso queira pode customizar algumas variáveis de ambiente editando o arquivo `.env`.


## Crie MongoDB

```shell
$ docker run --name mongo-latest -p 27017:27017 -d mongo
```

## Excute a aplicação de dev

```shell
$ make dev
```

## Excute a aplicação de dev via docker

Primeiro faço um build da minha imagem

```shell
$ docker build -t api_users .
```

Em seguida executar o container a partir da imagem criada

```shell
$ docker run -itd --name flask_api_users -p 5000:5000  -e SECRET_KEY=hard-secret-key --link mongo-latest:dbserver -e MONGODB_URI=mongodb://dbserver:27017/api-users api_users
```

## Excute a aplicação de prod via docker

Essa build executa o `gunicorn` ao invés do `python application.py`

```shell
$ docker build -t api_users_prd -f Dockerfile-prd .
```

Em seguida executar o container a partir da imagem criada

```shell
$ docker run -itd --name flask_api_users_prd -p 5001:5000  -e SECRET_KEY=hard-secret-key --link mongo-latest:dbserver -e MONGODB_URI=mongodb://dbserver:27017/api-users api_users_prd
```

## Roadmap

* Capítulo 1: [Introdução, configuração e Hello World](https://www.lucassimon.com.br/2018/06/serie-api-em-flask---parte-1---introducao-configuracao-e-hello-world/)

* Capítulo 2: [Organizando as dependências e requerimentos](https://lucassimon.com.br/2018/06/serie-api-em-flask---parte-2---organizando-as-dependencias-e-requerimentos/)

* Capítulo 3: [Configurando o pytest e nosso primeiro teste](https://lucassimon.com.br/2018/06/serie-api-em-flask---parte-3---configurando-o-pytest-e-nosso-primeiro-teste/)

* Capítulo 4: [Configurando o Makefile](https://lucassimon.com.br/2018/06/serie-api-em-flask---parte-4---configurando-o-makefile/)

* Capítulo 5: [Adicionando o MongoDB a API](https://lucassimon.com.br/2018/07/serie-api-em-flask---parte-5---mongodb/)

* Capítulo 6: [Criando e testando nosso modelo de usuários](https://lucassimon.com.br/2018/10/serie-api-em-flask---parte-6---criando-e-testando-nosso-modelo-de-usuarios/)

* Capítulo 7: [Criando usuários](https://lucassimon.com.br/2018/10/serie-api-em-flask---parte-7---criando-usuarios/)

* Capítulo 8: [Listando usuários](https://lucassimon.com.br/2018/10/serie-api-em-flask---parte-8---listando-usuarios/)

* Capítulo 9: [Buscando usuários](https://lucassimon.com.br/2018/10/serie-api-em-flask---parte-9---buscando-usuarios/)

* Capítulo 10: [Editando um usuário](https://lucassimon.com.br/2018/10/serie-api-em-flask---parte-10---editando-um-usuario/)

* Capítulo 11: [Deletando um usuário](https://lucassimon.com.br/2018/10/serie-api-em-flask---parte-11---deletando-um-usuario/)

* Capítulo 12: [Autênticação por JWT](https://lucassimon.com.br/2018/10/serie-api-em-flask---parte-12---autenticacao-por-jwt/)
