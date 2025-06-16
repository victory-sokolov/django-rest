from typing import Any
from django.core.management.commands.test import Command as BaseCommand


class Command(BaseCommand):
    def handle(
        self,
        *test_labels: dict[str, str],
        **options: Any,
    ) -> str | None:
        options["interactive"] = False
        return super().handle(*test_labels, **options)
