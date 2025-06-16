import json
import logging
from logging import LogRecord
from datetime import datetime


class FilebeatFormatter(logging.Formatter):
    def format(self, record: LogRecord) -> str:
        data = {
            "message": record,
            "@timestamp": datetime.now(),
            "log.level": record.levelname.upper(),
            "log.name": record.name,
        }

        return json.dumps(data, default=str)
