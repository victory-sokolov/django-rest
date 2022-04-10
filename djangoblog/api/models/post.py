import uuid
from django.db import models

from djangoblog.api.models.author import Author
from djangoblog.api.models.category import Category
from ckeditor.fields import RichTextField


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    title = models.CharField(max_length=200)
    body = RichTextField(blank=True, null=True)
    category = models.ManyToManyField(Category, max_length=100)
    author = models.ForeignKey(Author, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "posts"

    def __str__(self):
        return self.title
