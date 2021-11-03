from django.contrib import admin
from django.urls import path
from djangoblog.api.v1.posts.views import ArticleView, SingleArticle
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/post/", ArticleView.as_view(), name="posts"),
    path("api/v1/post/<int:pk>", SingleArticle.as_view(), name="post"),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]
