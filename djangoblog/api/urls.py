from django.urls import path
from drf_spectacular.views import (
    SpectacularJSONAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from rest_framework import routers

from djangoblog.api.v1.posts import views
from djangoblog.api.v1.token.views import RefreshTokenView, TokenView

router = routers.SimpleRouter()
# router.register(r"post", views.ArticleListView.as_view(), basename="post")

urlpatterns = [
    # re_path(r"^v1/", include((router.urls))),
    path("v1/post/", views.ArticleListView.as_view(), name="posts"),
    path("v1/post/<uuid:id>/", views.SingleArticleView.as_view(), name="post"),
    path("schema.json", SpectacularJSONAPIView.as_view(), name="schema"),
    # tokens endpoints
    path("v1/token", TokenView.as_view(), name="token_obtain_pair"),
    path("v1/refresh", RefreshTokenView.as_view(), name="token_refresh"),
    # Schemas
    path(
        "v1/schema.json",
        SpectacularJSONAPIView.as_view(api_version="v1"),
        name="schema-json-v1",
    ),
    # Docs
    path(
        "v1/docs",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "v1/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]
