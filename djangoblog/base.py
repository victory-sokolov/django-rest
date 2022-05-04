from django.db import models


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    ``created`` and ``modified`` fields.
    """

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=("created_at"),
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name=("updated_at"))

    class Meta:
        abstract = True
