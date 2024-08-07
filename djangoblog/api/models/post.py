from uuid import uuid4

from ckeditor.fields import RichTextField
from django.db import models

from djangoblog.api.models.managers import TagQuerySet
from djangoblog.base import TimeStampedModel
from djangoblog.models import UserProfile

STATUS = ((0, "Draft"), (1, "Publish"))


class Tags(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    tag = models.CharField(max_length=20)
    slug = models.SlugField(max_length=20, unique=True, null=True)

    objects = TagQuerySet.as_manager()

    class Meta:
        db_table = "post_tag"

    def __str__(self):
        return self.tag


class PostPermissions(models.Model):
    code_name = models.CharField(max_length=256, unique=True)
    description = models.CharField(max_length=256)


class Post(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid4)
    user = models.ForeignKey(UserProfile, null=True, on_delete=models.CASCADE)
    tags = models.ManyToManyField("Tags", blank=True, related_name="posts")
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, null=True)
    content = RichTextField(blank=True, null=True)
    draft = models.BooleanField(default=False)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    favorites = models.IntegerField(default=0)

    permissions = models.ManyToManyField(
        PostPermissions,
        blank=True,
        related_name="permissions",
    )

    class Meta:
        db_table = "posts"
        ordering = ("created_at",)

    def __str__(self) -> str:
        return self.title


class PostComments(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    post_id = models.ForeignKey(Post, null=True, on_delete=models.CASCADE)
    comment = models.TextField()
    likes = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "post_comments"
