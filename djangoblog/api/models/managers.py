from __future__ import annotations
from typing import TYPE_CHECKING
from typing import List

from django.db.models import QuerySet

if TYPE_CHECKING:
    from djangoblog.api.models.post import Tags


class TagQuerySet(QuerySet):
    """Custom TagQuerySet implementation."""

    def create_if_not_exist(self, tags: List[str]) -> QuerySet[Tags]:
        """Create Tag if it doesn't exists."""
        tag_set = self.values_list("tag", flat=True)
        for t in tags:
            if t not in tag_set:
                self.create(tag=t, slug=t.lower().replace(" ", "-"))
        return self.filter(tag__in=tags)
