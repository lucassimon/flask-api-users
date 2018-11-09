import os

bind = "127.0.0.1:9000"
workers = (os.sysconf("SC_NPROCESSORS_ONLN") * 2) + 1
loglevel = "error"
pidfile = "/home/apiflask/run/app.pid"
accesslog = "/home/apiflask/logs/gunicorn/access-app.log"
errorlog = "/home/apiflask/logs/gunicorn/error-app.log"
secure_scheme_headers = {
    'X-FORWARDED-PROTOCOL': 'http',
    'X-FORWARDED-PROTO': 'http',
}
