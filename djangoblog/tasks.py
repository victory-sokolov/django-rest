import logging

import celery
from django.db.models import Prefetch
from djangoblog.api.models.post import Post
from djangoblog.celery_app import app
from djangoblog.api.v1.posts.serializers import PostSerializer
logger = logging.getLogger(__name__)


class PostTask(celery.Task):
    name = "djangoblog.tasks.PostTask"
    POST_PER_PAGE = 10

    def run(self):
        logger.info("Retrieving all posts.")
        select_posts = Post.objects.select_related("user").all().order_by("-created_at")
        posts = Post.objects.prefetch_related(Prefetch('tags', queryset=select_posts)).all()
        serializer = PostSerializer(data=posts, many=True)
        if serializer.is_valid():
            serializer.save()
            return serializer.data

app.register_task(PostTask())
