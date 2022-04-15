from django.urls import path, include
from django.urls.conf import re_path
from drf_spectacular.views import (
    SpectacularJSONAPIView,
    SpectacularSwaggerView,
)
from rest_framework import routers
from djangoblog.api.v1.posts.views import ArticleView

router = routers.SimpleRouter()
router.register(r"post", ArticleView, basename="posts")

urlpatterns = [
    re_path(r"^v1/", include((router.urls))),
    path("schema/", SpectacularJSONAPIView.as_view(), name="schema"),
    # Schemas
    path(
        "v1/schema.json",
        SpectacularJSONAPIView.as_view(api_version="v1"),
        name="schema-json-v1",
    ),
    path(
        "v2/schema.json",
        SpectacularJSONAPIView.as_view(api_version="v2"),
        name="schema-json-v2",
    ),
    # Docs
    path(
        "docs",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="api-documentation",
    ),
]
