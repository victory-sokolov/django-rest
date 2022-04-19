from typing import Union
from uuid import uuid4
from django.db import models
from django.db.models.query import QuerySet

from djangoblog.api.models.category import Category
from ckeditor.fields import RichTextField

from djangoblog.base import TimeStampedModel
from djangoblog.models import UserProfile


class Post(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid4)
    user = models.ForeignKey(UserProfile, null=True, on_delete=models.CASCADE)
    tag = models.ManyToManyField("Tags", blank=True, related_name="posts")
    title = models.CharField(max_length=200)
    body = RichTextField(blank=True, null=True)
    category = models.ManyToManyField(Category, max_length=100)
    draft = models.BooleanField(default=False)
    post_views = models.IntegerField(default=0)
    post_likes = models.IntegerField(default=0)
    post_favorites = models.IntegerField(default=0)

    class Meta:
        db_table = "posts"
        ordering = ("created_at",)

    def __str__(self) -> str:
        return self.title


class Tags(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    tag = models.CharField(max_length=20)
    slug = models.SlugField(max_length=20, unique=True, null=True)

    class Meta:
        db_table = "post_tag"

    @classmethod
    def create_if_not_exist(cls, tags: "list[str]") -> "QuerySet[Tags]":
        """Create Tag if it doesn't exists."""
        tag_set = Tags.objects.values_list("tag", flat=True)

        for t in tags:
            if t not in tag_set:
                Tags.objects.create(tag=t, slug=t.lower().replace(" ", "-"))

        return Tags.objects.filter(tag__in=tags)

    def __str__(self):
        return self.tag


class PostComments(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    post_id = models.ForeignKey(Post, null=True, on_delete=models.CASCADE)
    comment = models.TextField()
    likes = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "post_comments"
