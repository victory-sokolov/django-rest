from typing import Any
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Get a list of all permissions available in the system."

    def handle(self, *args: Any, **options: Any) -> None:
        permissions = set()

        # CreateModel a temporary superuser and use it to get permissions
        tmp_superuser = get_user_model()(is_active=True, is_superuser=True)

        for backend in auth.get_backends():
            if hasattr(backend, "get_all_permissions"):
                permissions.update(backend.get_all_permissions(tmp_superuser))

        sorted_list_of_permissions = sorted(list(permissions))
        self.stdout.write("\n".join(sorted_list_of_permissions))
