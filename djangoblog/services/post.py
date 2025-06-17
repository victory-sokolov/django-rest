import logging
from typing import Any

from djangoblog.api.v1.posts.serializers import PostSerializer
from djangoblog.api.v1.posts.types import UserId
from djangoblog.repository.post import PostRepository
from djangoblog.repository.tags import TagsRepositry
from djangoblog.repository.user import UserRepository

logger = logging.getLogger(__name__)


class PostService:
    def __init__(self) -> None:
        self.post_repository = PostRepository()
        self.use_repository = UserRepository()
        self.tags_repository = TagsRepositry()

    def get_all(self) -> dict[str, Any] | None:
        fields = ["id", "title", "slug", "user", "tags", "content"]
        posts = self.post_repository.get_all(fields)
        logger.info(f"Retrieving all posts. Found {posts.count()} posts.")

        serializer = PostSerializer(posts, many=True)

        try:
            return serializer.data
        except Exception as e:
            logger.error("Failed to fetch posts", exc_info=e)

    def create(self, user_id: UserId, tags: list[str], data: dict[str, str]) -> None:
        user = self.use_repository.get(user_id)
        tag_set = self.tags_repository.create(tags)
        post = self.post_repository.create(data, user)

        for tag in tag_set:
            post.tags.add(tag)

        logger.info(
            f"New post with {post.id} has been created",
            extra={"post_id": post.id},
        )
