# -*- coding: utf-8 -*-
from json import dumps


from flask import g

from jwt import encode as jwt_encode

from apps.users.models import User


class ProducerSignUp:

    def __init__(self, queue: str):

        if not isinstance(queue, str):
            raise ValueError('Verifique a uri do sistema de filas')

        conn = g.rabbit
        self.queue = queue
        self.channel = conn.channel()
        self.channel.queue_declare(queue=queue, durable=True)


    def publish(self, user: {}, token):
        '''
        Publish a message in default exchange
        '''

        from apps.api import api  # solve ciclic import
        from apps.users.resources import ConfirmEmail
        url = api.url_for(ConfirmEmail, token=token, _external=True)

        context = { "data": user, "url": url }

        message = self.message(name='Api-Users', to=user.get('email'), **context)

        try:
            body = dumps(message)

        except Exception as e:
            raise e

        self.channel.basic_publish(exchange='', routing_key=self.queue, body=body)

    def message(
        self, name: str, to: str,
        subject: str = 'Confirme o email.',
        ffrom: str = 'no-reply@api-users',
        **kwargs
    ):

        message = {
            "app": name, "from": ffrom, "to": to, "subject": subject,
            "body": '''
            Você se registrou em nossa plataforma {{app}}.
            Precisamos que ative seu email na seguinte {{url}}
            '''
        }

        if 'context' in kwargs:
            message['context'] = kwargs['context']

        return message
