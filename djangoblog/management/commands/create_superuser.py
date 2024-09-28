from typing import Any

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandParser


class Command(BaseCommand):
    """
    Create a superuser if none exist
    Example:
        manage.py create_superuser --user=admin --password=changeme
    """

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("--user", required=True)
        parser.add_argument("--password", required=True)
        parser.add_argument("--email", default="admin@example.com")

    def handle(self, *args: Any, **options: Any) -> None:
        user_model = get_user_model()
        username = options["user"]
        password = options["password"]
        email = options["email"]

        user = user_model.objects.filter(email=email)

        if user.exists():
            self.stdout.write(f"User with email {email} already exists")
            return

        user_model.objects.create_superuser(
            username=username,
            password=password,
            email=email,
        )

        self.stdout.write(f'Local user "{username}" was created')
