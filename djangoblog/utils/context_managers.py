import logging
from typing import Optional

from django.core.cache import caches
from tblib import Traceback

logger = logging.getLogger(__name__)


class RedisLock:
    """RedisLock - used for Celery tasks."""

    def __init__(self, lock_id: str, oid: str) -> None:
        self.lock_id = lock_id
        self.oid = oid
        self.lock_acquired = False

    def __enter__(self) -> bool:
        """Acquire lock."""
        self.lock_acquired = caches["tasks"].set(self.lock_id, self.oid)
        return self.lock_acquired

    def __exit__(
        self,
        exc_type: Optional[Exception],
        exc_val: Optional[str],
        exc_tb: Optional[Traceback],
    ) -> bool:
        """Delete lock key on exit."""
        caches["tasks"].delete(self.lock_id)
        if exc_type:
            logger.error(f"An exception occurred: {exc_val} - {exc_tb}")
            return False

        return True
