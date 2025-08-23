import logging

logger = logging.getLogger(__name__)


class LogFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        excluded_paths = ["/health/app"]
        message = record.getMessage()

        return not any(path in message for path in excluded_paths)
