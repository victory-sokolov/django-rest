from django.contrib import admin
from django.urls import path, include
from django.urls.conf import re_path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularJSONAPIView,
    SpectacularSwaggerView,
)
from rest_framework import routers

from djangoblog.api.v1.posts.views import ArticleView, SingleArticle


router = routers.SimpleRouter()
router.register(r"^(?P<version>(v1))/posts", ArticleView.as_view(), basename="posts")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/post/<int:pk>", SingleArticle.as_view(), name="post"),
    # Api v2
    path("api/v2/post/", ArticleView.as_view(), name="posts"),
    re_path(r"^v1/post/", ArticleView.as_view(), name="posts"),
    re_path(r"^v2/post/", ArticleView.as_view(), name="posts"),
    path("api/schema/", SpectacularJSONAPIView.as_view(), name="schema"),
    # Schemas
    path(
        "api/v1/schema.json",
        SpectacularJSONAPIView.as_view(api_version="v1"),
        name="schema-json-v1",
    ),
    path(
        "api/v2/schema.json",
        SpectacularJSONAPIView.as_view(api_version="v2"),
        name="schema-json-v2",
    ),
    # Docs
    path(
        "api/docs",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="api-documentation",
    ),
    # path("", include(router.urls)),
]
