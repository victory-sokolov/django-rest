import logging

import celery

from djangoblog.api.models.post import Post
from djangoblog.api.v1.posts.serializers import PostSerializer
from djangoblog.celery import app

logger = logging.getLogger(__name__)


class PostTask(celery.Task):
    name = "PostTask"
    POST_PER_PAGE = 10

    def run(self):
        selected_posts = (
            Post.objects.select_related("user")
            .all()
            .order_by("-created_at")
            .prefetch_related("tags")
        )
        logger.info(f"Retrieving all posts. Found {selected_posts.count()} posts")
        serializer = PostSerializer(selected_posts, many=True)
        try:
            return serializer.data
        except Exception as e:
            logger.error("Failed to fetch posts", exc_info=e)


app.register_task(PostTask())
