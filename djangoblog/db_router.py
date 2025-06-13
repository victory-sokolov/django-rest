from enum import StrEnum
from typing import Any, Optional


class Replcias(StrEnum):
    DEFAULT = "default"
    DB_READ = "read_replica"


class CustomRouter:
    def db_for_read(self, model: Any, **hints: dict[str, Any]) -> Replcias:
        return Replcias.DEFAULT
        # Enable when docker is properly configured to server PostgreSQL replicas
        # return Replcias.DB_READ

    def db_for_write(self, model: Any, **hints: dict[str, Any]) -> Replcias:
        return Replcias.DEFAULT

    def allow_relation(self, obj1: Any, obj2: Any, **kwargs: dict[str, Any]) -> bool:
        db_set = {"default", "read_replica"}
        if obj1._state.db in db_set and obj2._state.db in db_set:
            return True
        return False

    def allow_migrate(
        self,
        _db: Any,
        _app_label: str,
        _model_name: Optional[str] = None,
        **hints: dict[str, Any],
    ) -> bool:
        return True
