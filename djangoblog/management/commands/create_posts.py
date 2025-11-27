import time
from typing import Any

from django.core.management.base import BaseCommand, CommandParser

from djangoblog.factory import AccountFactory


class Command(BaseCommand):
    """Populate database with random posts."""

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("--count", required=True)

    def handle(self, *args: list[Any], **options: Any) -> None:
        count = int(options["count"])

        t0 = time.perf_counter()
        AccountFactory.create_batch(count)
        elapsed = time.perf_counter() - t0

        self.stdout.write(
            self.style.SUCCESS(
                f"Generated {count} accounts in {elapsed:.3f}s "
                f"({elapsed * 1000 / count:.1f}ms / account)"
            )
        )
