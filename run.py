# -*- coding: utf-8 -*-

# Python
from os import getenv
from os.path import dirname, isfile, join

# Third
from dotenv import load_dotenv


# a partir do arquivo atual adicione ao path o arquivo .env
_ENV_FILE = join(dirname(__file__), '.env')

# existindo o arquivo faça a leitura do arquivo através da função load_dotenv
if isfile(_ENV_FILE):
    load_dotenv(dotenv_path=_ENV_FILE)


# Apps
from apps.app import create_app

# instancia nossa função factory criada anteriormente
app = create_app()

if __name__ == '__main__':
    ip = '0.0.0.0'
    port = app.config['PORT']
    debug = app.config['DEBUG']

    # executa o servidor web do flask
    app.run(
        host=ip, debug=debug, port=port, use_reloader=debug
    )
