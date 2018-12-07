# -*- coding: utf-8 -*-

# Third
from pika import BlockingConnection, URLParameters
from flask import current_app


class RabbitMQ:

    @staticmethod
    def connect():
        params = URLParameters(current_app.config.get('AMQP_URI'))
        # number of socket connection attempts
        params.connection_attempts = 7
        # interval between socket connection attempts; see also connection_attempts.
        params.retry_delay = 300
        # AMQP connection heartbeat timeout value for negotiation during connection
        # tuning or callable which is invoked during connection tuning
        params.heartbeat = 600
        # None or float blocked connection timeout
        params.blocked_connection_timeout = 300
        try:
            return BlockingConnection(params)
        except Exception as e:
            raise
