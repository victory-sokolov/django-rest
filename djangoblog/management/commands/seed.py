import logging
import random

from django.core.management.base import BaseCommand, CommandParser
from faker import Faker
from djangoblog.api.models.post import Post
from djangoblog.models import UserProfile


class Command(BaseCommand):
    help = "Seed database for testing and development"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("--amount", type=str, help="amount of posts to generate")

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
        post = Post(
            user=random.choice(users),
            title=f"{fake.company()} {fake.country()}",
            content=fake.text(),
        )
        posts.append(post)

    Post.objects.bulk_create(posts)
