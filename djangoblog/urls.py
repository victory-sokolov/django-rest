from django.contrib import admin
from django.urls import include, path
from .view import index, post

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index),
    path("post/", post),
    path("api/", include("djangoblog.api.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
]
