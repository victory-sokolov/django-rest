import logging
import requests

from django.core.management.base import BaseCommand, CommandParser
from requests.models import HTTPError
from djangoblog.models.posts import Post

class Command(BaseCommand):
    help='Seed database for testing and development'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('--amount', type=str, help="amount of posts to generate")

    def handle(self, *args, **options):
        logging.info('Fetching posts...')
        run_seed(self)
        self.stdout.write('Post fetching done.')


def clear_data():
    """Deletes all the table data"""
    print("Delete Address instances")
    # Post.objects.all().delete()

def fetch_posts():
    response = requests.get(f'https://jsonplaceholder.typicode.com/posts')
    if response.status_code == 200:
        return response.json()

    raise HTTPError(response.json())

def run_seed(self):
    response = fetch_posts()
    print(response)

    for article in response:
        post = Post(
            id = article['id'],
            user_id = article['userId'],
            title = article['title'],
            body = article['body']
        )
        post.save()
