import uuid
from django.db import models


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    category_id = models.IntegerField()
    category = models.CharField(max_length=255)

    def __str__(self):
        return self.category

    class Meta:
        db_table = "category"
