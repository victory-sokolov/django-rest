import json
import logging
from datetime import datetime


class FilebeatFormatter(logging.Formatter):
    def format(self, record) -> str:
        data = {
            "message": record,
            "@timestamp": datetime.now(),
            "log.level": record.levelname.upper(),
            "log.name": record.name,
        }

        return json.dumps(data, default=str)
