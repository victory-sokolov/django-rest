from uuid import uuid4
from django.db import models

from djangoblog.api.models.category import Category
from ckeditor.fields import RichTextField

from djangoblog.base import TimeStampedModel
from djangoblog.models import UserProfile


class Post(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid4)
    user = models.ForeignKey(UserProfile, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    body = RichTextField(blank=True, null=True)
    category = models.ManyToManyField(Category, max_length=100)
    draft = models.BooleanField(default=False)
    post_views = models.IntegerField(default=0)
    post_likes = models.IntegerField(default=0)
    post_favorites = models.IntegerField(default=0)

    class Meta:
        db_table = "posts"

    def __str__(self):
        return self.title


class PostComments(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    post_id = models.ForeignKey(Post, null=True, on_delete=models.CASCADE)
    comment = models.TextField()
    likes = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "post_comments"
