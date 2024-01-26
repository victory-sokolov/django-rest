import logging
import random

from django.core.management.base import BaseCommand, CommandParser
from faker import Faker

from djangoblog.api.models.post import Post
from djangoblog.models import UserProfile
from djangoblog.utils.utils import slugify


class Command(BaseCommand):
    help = "Seed database for testing and development"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "-a",
            "--amount",
            type=int,
            help="amount to generate",
        )

    def handle(self, *args, **options):
        logging.info("Adding new posts")
        amount = int(options["amount"])
        run_seed(amount)
        self.stdout.write(f"Added {amount} posts")


def clear_data():
    """Deletes all the table data"""
    logging.warning("Deleting all Posts")
    Post.objects.all().delete()


def run_seed(amount: int):
    fake = Faker()
    users = UserProfile.objects.all()
    posts = []
    for _ in range(amount):
        title = f"{fake.company()} {fake.country()}"
        post = Post(
            user=random.choice(users),
            title=title,
            content=fake.text(),
            slug=slugify(title),
        )
        posts.append(post)

    Post.objects.bulk_create(posts)
