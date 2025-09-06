import os

from djangoblog.logger import date_fmt

FORMATTERS = {
    "verbose": {
        "format": (
            "[{levelname}] {asctime} | Logger: {name} | "
            "Thread: {threadName} | Process: {process} | "
            "File: {filename}:{lineno} | "
            "Function: {funcName} | Message: {message}"
        ),
        "datefmt": date_fmt,
        "style": "{",
    },
    "simple": {
        "format": "[{levelname}] {asctime} | {name} | {message}",
        "datefmt": date_fmt,
        "style": "{",
    },
    "rich": {  # Assuming you use RichHandler
        "datefmt": date_fmt,
    },
    "json": {  # Keep your Filebeat/ELK formatter
        "class": "djangoblog.formatters.FilebeatFormatter",
    },
}

LOGGERS = {
    "django": {
        "handlers": ["console"],
        "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
        "filters": ["exclude_logs"],
        "propagate": True,
    },
    "django.request": {
        "handlers": ["console"],
        "level": "INFO",
        "propagate": True,
    },
    "django.template": {
        "handlers": ["console"],
        "level": "DEBUG",
        "propagate": True,
    },
    # Log DB queries
    "django.db.backends": {
        "level": "DEBUG",
        "handlers": ["console"],
        "propagate": True,
    },
    "gunicorn.error": {
        "handlers": [
            "console",
        ],
        "level": "INFO",
    },
    "gunicorn.access": {
        "handlers": [
            "console",
        ],
        "level": "INFO",
    },
    "psycopg.pool": {
        "handlers": ["console"],
        "level": "INFO",
    },
}

LOGGING_HANDLERS = {
    "base": {
        "class": "logging.StreamHandler",
        "level": "INFO",
        "formatter": "simple",
    },
    "console": {
        "class": "logging.StreamHandler",
        "formatter": "verbose",
        "level": "INFO",
        "filters": ["exclude_logs"],
    },
    "file": {
        "class": "logging.FileHandler",
        "formatter": "json",
        "filename": "/var/log/djangoblog.log",
        "delay": True,
    },
    "rich-console": {
        "class": "rich.logging.RichHandler",
        "formatter": "rich",
        "level": "INFO",
        "filters": ["exclude_logs"],
    },
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "exclude_logs": {
            "()": "djangoblog.filter.LogFilter",
        },
    },
    "formatters": FORMATTERS,
    "handlers": LOGGING_HANDLERS,
    "loggers": LOGGERS,
    "root": {
        "handlers": [],
        "level": "WARNING",
        "propagate": True,
        "filters": ["exclude_logs"],
    },
}
