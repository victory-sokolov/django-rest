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
        logger.info("Retrieving all posts.")
        selected_posts = (
            Post.objects.select_related("user")
            .all()
            .order_by("-created_at")
            .prefetch_related("tags")
        )
        serializer = PostSerializer(data=selected_posts, many=True)
        if not serializer.is_valid():
            logger.error("Failed to fetch posts", extra=serializer.errors)

        logger.info(f"Successfully retrieved {len(selected_posts)} posts")
        serializer.save()
        return serializer.data


app.register_task(PostTask())
