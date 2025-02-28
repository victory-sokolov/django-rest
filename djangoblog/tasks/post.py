import logging

import celery

from djangoblog.api.models.post import Post, Tags
from djangoblog.api.v1.posts.serializers import PostSerializer
from djangoblog.celery import app
from djangoblog.models import UserProfile

logger = logging.getLogger(__name__)


class GetPostsTask(celery.Task):
    """GetPostsTask."""

    name = "GetPostTask"
    expires = 600
    POST_PER_PAGE = 20

    def run(self):
        fields = ["id", "title", "slug", "user", "tags", "content"]
        selected_posts = (
            Post.objects.select_related("user")
            .prefetch_related("tags")
            .only(*fields)
            .order_by("-created_at")
        )
        logger.info(f"Retrieving all posts. Found {selected_posts.count()} posts.")
        serializer = PostSerializer(selected_posts, many=True)
        try:
            return serializer.data
        except Exception as e:
            logger.error("Failed to fetch posts", exc_info=e)


class CreatePostsTask(celery.Task):
    """CreatePostsTask."""

    name = "CreatePostTask"

    def run(self, data: dict):
        user = UserProfile.objects.get(id=data["user_id"])
        post = Post.objects.create(
            title=data["title"],
            content=data["content"],
            slug=data["slug"],
            user=user,
            draft=data.get("is_draft"),
        )

        tag_set = Tags.objects.create_if_not_exist(data["tags"])
        for tag in tag_set:
            post.tags.add(tag)

        logger.info(
            f"New post with {post.id} has been created",
            extra={"post_id": post.id},
        )


app.register_task(GetPostsTask())
app.register_task(CreatePostsTask())
