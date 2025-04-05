from django.db.models import QuerySet

from djangoblog.api.models.post import Tags
from djangoblog.repository.base import IRepository


class TagsRepositry(IRepository):
    def __init__(self) -> None:
        self.tag = Tags.objects

    def create(self, tags: list[str]) -> QuerySet[Tags]:
        return self.tag.create_if_not_exist(tags)

    def get(self) -> Tags: ...

    def get_all(self) -> Tags: ...
