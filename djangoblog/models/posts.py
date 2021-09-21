from django.db import models

class Posts(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    title = models.CharField(max_length=200)
    body = models.TextField()

    class Meta:
        db_table = 'posts'