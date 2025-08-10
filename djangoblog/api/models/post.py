from typing import Any
from uuid import uuid4

from ckeditor.fields import RichTextField
from django.db import models
from django.utils.timezone import now

from djangoblog.api.models.managers import TagQuerySet
from djangoblog.base import TimeStampedModel
from djangoblog.models import UserProfile

STATUS = ((0, "Draft"), (1, "Publish"))


class Tags(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    tag = models.CharField(max_length=20)
    slug = models.SlugField(max_length=20, unique=True)

    objects = TagQuerySet.as_manager()

    class Meta:
        db_table = "post_tag"

    def __str__(self) -> str:
        return self.tag


class PostPermissions(models.Model):
    code_name = models.CharField(max_length=256, unique=True)
    description = models.CharField(max_length=256)

    class Meta:
        db_table = "post_permission"


class Post(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid4)
    user = models.ForeignKey(
        UserProfile,
        null=True,
        on_delete=models.CASCADE,
        related_name="user",
    )
    tags = models.ManyToManyField("Tags", blank=True, related_name="posts")
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    content = RichTextField(blank=True)
    draft = models.BooleanField(default=False)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    favorites = models.IntegerField(default=0)

    permissions = models.ManyToManyField(
        PostPermissions,
        blank=True,
        related_name="permissions",
    )

    def save(self, *args: Any, **kwargs: Any) -> None:
        if self.created_at is None:
            self.created_at = now()

        super().save(*args, **kwargs)

    class Meta:
        db_table = "posts"
        ordering = ("created_at",)
        indexes = [models.Index(fields=["title", "created_at"])]

    def __str__(self) -> str:
        return self.title


class PostComments(models.Model):
    """PostComments."""

    id = models.UUIDField(primary_key=True, default=uuid4)
    post_id = models.ForeignKey(
        Post,
        null=True,
        on_delete=models.CASCADE,
        related_name="post_id",
    )
    comment = models.TextField()
    likes = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "post_comments"
