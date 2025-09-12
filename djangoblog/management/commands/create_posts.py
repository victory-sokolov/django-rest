from sys import stdout
from typing import Any

from django.core.management.base import BaseCommand, CommandParser

from djangoblog.factory import AccountFactory


class Command(BaseCommand):
    """Populate database with random posts."""

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("--count", required=True)

    def handle(self, *args: list[Any], **options: Any) -> None:
        count = int(options["count"])
        AccountFactory.create_batch(count)
        stdout.write(f"Generated {count} posts\n")
