from rest_framework import routers
from .posts.views import ArticleView

router = routers.SimpleRouter()

router.register(r"post", ArticleView)
