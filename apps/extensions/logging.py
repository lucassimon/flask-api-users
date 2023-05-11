# Python
import logging

# Third
import structlog


def configure_logging(debug=False):

    default = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.CallsiteParameterAdder(
            {
                structlog.processors.CallsiteParameter.FILENAME,
                structlog.processors.CallsiteParameter.FUNC_NAME,
                structlog.processors.CallsiteParameter.LINENO,
                structlog.processors.CallsiteParameter.PATHNAME,
            }
        ),
    ]
    production = default + [structlog.processors.dict_tracebacks, structlog.processors.JSONRenderer()]

    development = default + [
        structlog.dev.set_exc_info,
        structlog.dev.ConsoleRenderer(exception_formatter=structlog.dev.rich_traceback),
    ]

    processors = development if debug else production

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(logging.NOTSET),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=False,
    )


def make_logger(debug: bool):
    configure_logging(debug)
    log = structlog.get_logger()
    return log
