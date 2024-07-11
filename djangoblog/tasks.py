import logging

import celery

from djangoblog.api.models.post import Post, Tags
from djangoblog.api.v1.posts.serializers import PostSerializer
from djangoblog.celery import app
from djangoblog.models import UserProfile

logger = logging.getLogger(__name__)


class GetPostsTask(celery.Task):
    name = "GetPostTask"
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


class CreatePostsTask(celery.Task):
    name = "CreatePostTask"

    def run(self, data: dict):
        print("Task id", self.request.id)
        user = UserProfile.objects.get(id=data["user_id"])
        post = Post.objects.create(
            title=data["title"],
            content=data["content"],
            user=user,
            draft=data.get("is_draft"),
        )

        tag_set = Tags.objects.create_if_not_exist(data["tags"])
        for tag in tag_set:
            post.tags.add(tag)

        logger.info(f"New post with {post.id} has been created")

app.register_task(GetPostsTask())
app.register_task(CreatePostsTask())
