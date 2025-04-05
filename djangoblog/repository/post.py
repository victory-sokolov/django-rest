from typing import Any

from django.db.models import QuerySet

from djangoblog.api.models.post import Post
from djangoblog.models import UserProfile
from djangoblog.repository.base import IRepository


class PostRepository(IRepository):
    def __init__(self) -> None:
        self.post = Post.objects

    def get_all(self, fields: list[str]) -> QuerySet[Post]:
        selected_posts = (
            self.post.select_related("user")
            .prefetch_related("tags")
            .only(*fields)
            .order_by("-created_at")
        )
        return selected_posts

    def get(self) -> None: ...

    def create(self, data: dict[str, Any], user: UserProfile) -> Post:
        post = Post.objects.create(
            title=data["title"],
            content=data["content"],
            slug=data["slug"],
            user=user,
            draft=data.get("is_draft", False),
        )
        return post
