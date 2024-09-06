from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        print("Running copression.... ->>")
        print(settings.GS_BUCKET_NAME)
        print(settings.COMPRESS_STORAGE)
        print(settings.COMPRESS_URL)
        print(settings.COMPRESS_OFFLINE_MANIFEST_STORAGE)

        call_command("compress", force=True)
