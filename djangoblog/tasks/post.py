import logging

import celery

from djangoblog.celery import app
from djangoblog.services.post import PostService

logger = logging.getLogger(__name__)


class GetPostsTask(celery.Task):
    """GetPostsTask."""

    name = "GetPostTask"
    expires = 600
    POST_PER_PAGE = 20

    def __init__(self) -> None:
        self.post_service = PostService()

    def run(self):
        return self.post_service.get_all()


class CreatePostsTask(celery.Task):
    """CreatePostsTask."""

    name = "CreatePostTask"

    def __init__(self) -> None:
        self.post_service = PostService()

    def run(self, data: dict) -> None:
        return self.post_service.create(data["user_id"], data["tags"], data)


app.register_task(GetPostsTask())
app.register_task(CreatePostsTask())
