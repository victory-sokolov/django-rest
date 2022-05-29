import logging
from djangoblog.api.models.post import Post
from djangoblog.celery import app
from djangoblog.api.v1.posts.serializers import PostSerializer

logger = logging.getLogger(__name__)


@app.task(name="retrieve all posts")
def retrieve_all_posts():
    logger.info("Retrieving all posts.")
    posts = Post.objects.all().order_by("-created_at")
    serializer = PostSerializer(posts, many=True)
    return serializer.data
