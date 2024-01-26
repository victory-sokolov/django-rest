from rest_framework.exceptions import ValidationError


class PostException(Exception):
    @staticmethod
    def validation_error(error, field, **kwargs) -> ValidationError:
        data = {"details": error, "summary": f"Field {field} {error[0]}"}
        return ValidationError(data)
