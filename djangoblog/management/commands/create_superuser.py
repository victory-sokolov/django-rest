from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    """
    Create a superuser if none exist
    Example:
        manage.py create_superuser --user=admin --password=changeme
    """

    def add_arguments(self, parser):
        parser.add_argument("--user", required=True)
        parser.add_argument("--password", required=True)
        parser.add_argument("--email", default="admin@example.com")

    def handle(self, *args, **options):
        user = get_user_model()
        username = options["user"]
        password = options["password"]
        email = options["email"]
    
        if user.objects.exists():
            self.stdout.write(f"User with email {email} already exists")
            return

        user.objects.create_superuser(username=username, password=password, email=email)

        self.stdout.write(f'Local user "{username}" was created')
