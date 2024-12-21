import logging
from typing import Any

from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand, CommandParser
from faker import Faker

from djangoblog.models import UserProfile


class Command(BaseCommand):
    help = "Seed database witht users"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "-a",
            "--amount",
            type=int,
            help="amount of users to generate",
        )

    def handle(
        self,
        amount: int,
        *args: Any,
        **kwargs: Any,
    ):
        logging.info("Creating new users")
        run_seed(amount)
        self.stdout.write(f"Added {amount} users")


def run_seed(amount: int) -> None:
    fake = Faker()
    user_list = []
    for _ in range(amount):
        user = UserProfile(
            name=fake.name(),
            email=fake.email(),
            password=make_password(fake.password()),
        )
        user_list.append(user)

    UserProfile.objects.bulk_create(user_list)
