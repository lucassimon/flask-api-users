FROM python:3.11-alpine as base
ENV HOME=/home/app \
    POETRY_VIRTUALENVS_PATH=/home/app/venv \
    POETRY_HOME=/home/app/poetry \
    PATH="/home/app/venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN rm -rf /var/cache/apk/* && \
    apk --no-cache update && \
    apk add make && \
    apk add build-base && \
    apk add gcc && \
    apk add python3-dev && \
    apk add libffi-dev && \
    apk add musl-dev && \
    apk add openssl-dev && \
    apk add curl && \
    apk del build-base && \
    rm -rf /var/cache/apk/* && \
    python -m venv /home/app/venv && \
    /home/app/venv/bin/pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.path /home/app/venv && \
    poetry config virtualenvs.create false

# DEVLOPMENT
FROM base as dev
USER 1000:1000
WORKDIR $HOME

# CI
FROM dev as ci
WORKDIR $HOME
COPY . .
RUN source /home/app/venv/bin/activate && \
    poetry install --with dev,test,docs

# PROD
FROM ci as build
RUN rm -rf /home/app/venv && \
    python -m venv /home/app/venv && \
    pip install poetry && \
    poetry install --only main,prod --without dev,test,docs

# SHIPMENT

FROM base
WORKDIR $HOME
COPY --chown=nobody --from=build /home/app/venv /home/app/venv
COPY --chown=nobody --from=build ${HOME} ${HOME}
USER nobody
# ENTRYPOINT ["tail", "-f", "/dev/null"]
ENTRYPOINT [ "gunicorn", "--config", "gunicorn_settings.py", "-b", ":8080", "run:app" ]
