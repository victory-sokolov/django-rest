import logging
from typing import Any

from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

from djangoblog.constants import Roles

logger = logging.getLogger(__name__)


class CustomAccountManager(BaseUserManager):
    def create_superuser(
        self,
        email: str,
        name: str,
        password: str,
        **other_fields: Any,
    ) -> "UserProfile":
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)

        if other_fields.get("is_staff") is not True:
            raise ValueError("Superuser must be assigned to is_staff=True.")
        if other_fields.get("is_superuser") is not True:
            raise ValueError(
                "Superuser must be assigned to is_superuser=True.",
            )

        return self.create_user(email, name, password, **other_fields)

    def create_user(
        self,
        email: str,
        name: str,
        password: str,
        **other_fields: Any,
    ) -> "UserProfile":
        if not email:
            raise ValueError("You must provide an email address")

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **other_fields)
        user.set_password(password)
        user.save()
        logger.info(
            f"User with email {email} successfully created",
            extra={
                "user_id": user.id,
                "user_email": user.email,
            },
        )
        return user


class UserProfile(AbstractUser, PermissionsMixin):
    name = models.CharField(max_length=255, unique=False, default=None)
    email = models.EmailField(max_length=50, unique=True)
    email_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    password = models.CharField(max_length=100)
    profile_picture = models.ImageField(
        upload_to="avatars",
        default="avatars/default.png",
    )
    first_name = None
    last_name = None
    username = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    objects = CustomAccountManager()

    class Meta:
        db_table = "user_profile"

    def is_member(self, group_name: Roles) -> bool:
        return self.groups.filter(name=group_name.value).exists()

    def save(self, *args: list[Any], **kwargs: Any) -> None:
        # if self.is_member(Roles.STAFF):
        # permissions = Permission.objects.filter(codename__in=settings.STAFF_PERMISSIONS)
        # self.user_permissions.add(*permissions)
        # logger.info(f"Permissions {list(permissions)} added for user {self.email}")
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.email
