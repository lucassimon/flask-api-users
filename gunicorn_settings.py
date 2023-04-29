import os

bind = "127.0.0.1:9000"
workers = (os.sysconf("SC_NPROCESSORS_ONLN") * 2) + 1
threads = 4
worker_class = "gthread"
worker_connections = 1000
timeout = 60
keepalive = 30
daemon = False
pidfile = None
loglevel = "debug"
accesslog = "-"
errorlog = "-"
secure_scheme_headers = {
    'X-FORWARDED-PROTOCOL': 'http',
    'X-FORWARDED-PROTO': 'http',
}
