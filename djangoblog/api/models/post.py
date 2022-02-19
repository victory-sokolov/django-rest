import uuid
from django.db import models

from djangoblog.api.models.author import Author
from djangoblog.api.models.category import Category


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user_id = models.IntegerField()
    title = models.CharField(max_length=200)
    body = models.TextField()
    category = models.ManyToManyField(Category)
    author = models.ForeignKey(Author, null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = "posts"
