#!/bin/sh
source venv/bin/activate

case "$FLASK_ENV" in
    production)
        # exec gunicorn -b :$PORT --access-logfile - --error-logfile - "apps:create_app('production')"
        exec gunicorn -w $WORKERS -b :$PORT --access-logfile - --error-logfile - application:app
        ;;
    *) exec make run ;;
esac
