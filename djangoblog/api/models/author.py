import uuid
from django.db import models


class Author(models.Model):
    id = models.IntegerField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "author"
