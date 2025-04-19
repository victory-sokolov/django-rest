import os

from djangoblog.logger import date_fmt

FORMATTERS = {
    "verbose": {
        "format": "[{levelname}]: {asctime:s} {name} Thread: {threadName} {thread:d} | Module: {module} | File: {filename} {lineno:d} {name} {funcName} {process:d} {message}",
        "datefmt": date_fmt,
        "style": "{",
    },
    "simple": {
        "format": "[{levelname}]: {asctime:s} {name} | Module: {module} | File: {filename} {lineno:d} {funcName} {message}",
        "datefmt": date_fmt,
        "style": "{",
    },
    "rich": {
        "datefmt": date_fmt,
    },
    "json": {
        "class": "djangoblog.formatters.FilebeatFormatter",
    },
}

LOGGERS = {
    "django": {
        "handlers": ["console", "logstash"],
        "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
        "filters": ["exclude_logs"],
        "propagate": True,
    },
    "django.request": {
        "handlers": ["console", "logstash"],
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
            "logstash",
        ],
        "level": "INFO",
    },
    "gunicorn.access": {
        "handlers": [
            "console",
            "logstash",
        ],
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
    "logstash": {
        "level": "INFO",
        "class": "logstash.TCPLogstashHandler",
        "host": "logstash",
        "port": 50000,
        "version": 1,
        "message_type": "django",
        "fqdn": False,
        "tags": ["django.request"],
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
        "level": "INFO",
        "propagate": True,
        "filters": ["exclude_logs"],
    },
}
