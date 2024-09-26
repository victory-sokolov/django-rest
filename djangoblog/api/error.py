from typing import Any

from rest_framework.exceptions import ValidationError


class PostException(Exception):
    @staticmethod
    def validation_error(
        error: str | list, field: str, **kwargs: Any
    ) -> ValidationError:
        data = {"details": error, "summary": f"Field {field} {error[0]}"}
        return ValidationError(data)
