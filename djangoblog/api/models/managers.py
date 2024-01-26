from __future__ import annotations

from typing import TYPE_CHECKING, List

from django.db.models import QuerySet

if TYPE_CHECKING:
    from djangoblog.api.models.post import Tags


class TagQuerySet(QuerySet):
    """Custom TagQuerySet implementation."""

    def create_if_not_exist(self, tags: List[str]) -> QuerySet[Tags]:
        """Create Tag if it doesn't exists."""
        tag_set = list(self.values_list("tag", flat=True))

        for t in tags:
            tag = list(t.values())[0].lower()
            if not any(t.lower() == tag for t in tag_set):
                self.create(tag=tag, slug=tag.lower().replace(" ", "-"))

        return self.filter(tag__in=tag_set)
