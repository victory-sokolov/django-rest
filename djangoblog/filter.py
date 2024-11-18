import logging

logger = logging.getLogger(__name__)


class LogFilter(logging.Filter):
    def filter(self, record):
        excluded_paths = ["/metrics", "/healthcheck"]
        message = record.getMessage()

        return not any(path in message for path in excluded_paths)
