from django.db import models

class Post(models.Model):
    """Post model"""

    id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    title = models.CharField(max_length=200)
    body = models.TextField()

    class Meta:
        db_table = "posts"


class Category(models.Model):
    id = models.IntegerField(primary_key=True)
    category_id = models.IntegerField()
    category = models.CharField(max_length=50)


class Author(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "author"
