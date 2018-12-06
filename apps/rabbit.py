# -*- coding: utf-8 -*-

# Third
from pika import BlockingConnection, URLParameters


def connection_rabbit(uri):

    if uri:
        params = URLParameters(uri)
        params.socket_timeout = 5

        return BlockingConnection(params)

    return None
