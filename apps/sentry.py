import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration


def configure_sentry(dsn):
    sentry_sdk.init(dsn=dsn, integrations=[FlaskIntegration()])
