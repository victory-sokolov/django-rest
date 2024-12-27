from enum import Enum
from typing import Any, Optional


class Replcias(Enum):
    DEFAULT = "default"
    DB_READ = "read_replica"


class CustomRouter:
    def db_for_read(self, model: Any, **hints: Any):
        return Replcias.DEFAULT.value
        # Enable when docker is properly configured to server PostgreSQL replicas
        # return Replcias.DB_READ.value

    def db_for_write(self, model: Any, **hints: Any):
        return Replcias.DEFAULT.value

    def allow_relation(self, obj1: Any, obj2: Any, **kwargs: Any) -> bool:
        db_set = {"default", "read_replica"}
        if obj1._state.db in db_set and obj2._state.db in db_set:
            return True
        return False

    def allow_migrate(
        self,
        _db: Any,
        _app_label: str,
        _model_name: Optional[str] = None,
        **hints: Any,
    ) -> bool:
        return True
