from django.core.management.commands.test import Command as BaseCommand


class Command(BaseCommand):
    def handle(self, *test_labels, **options):
        options["interactive"] = False
        return super().handle(*test_labels, **options)
