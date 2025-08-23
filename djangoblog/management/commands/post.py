import logging
import secrets
from typing import Any

from django.core.management.base import BaseCommand, CommandParser
from faker import Faker

from djangoblog.api.models.post import Post
from djangoblog.models import UserProfile
from djangoblog.utilities import slugify


class Command(BaseCommand):
    help = "Seed database for testing and development"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "-a",
            "--amount",
            type=int,
            default=0,
            help="amount to generate",
        )
        parser.add_argument(
            "-d",
            "--delete",
            action="store_true",
            help="Delete all posts",
        )

    def handle(self, *args: Any, **options: Any) -> None:
        amount = options["amount"]
        delete = options["delete"]

        if delete and self.confirm_clear():
            delete_posts()
            self.stdout.write("Deleted all posts")
        elif amount:
            self.stdout.write("Adding new posts")
            run_seed(int(amount))
            self.stdout.write(f"Added {amount} posts")

    def confirm_clear(self) -> bool:
        """Confirm before deleting all posts"""
        self.stdout.write(
            self.style.WARNING(
                "WARNING: This will delete ALL posts. This action cannot be undone.",
            ),
        )
        confirmation = input("Are you sure you want to continue? [y/N]: ")
        return confirmation.lower() in ["y", "yes"]


def delete_posts() -> int:
    """Deletes all posts data"""
    logging.warning("Deleting all Posts")
    count, _ = Post.objects.all().delete()
    logging.info(f"Deleted {count} objects")
    return count


def run_seed(amount: int) -> None:
    fake = Faker()
    users = UserProfile.objects.all()
    posts = []
    for _ in range(amount):
        title = f"{fake.company()} {fake.country()}"
        post = Post(
            user=secrets.choice(users),
            title=title,
            content=fake.text(),
            slug=slugify(title),
        )
        posts.append(post)

    Post.objects.bulk_create(posts)
