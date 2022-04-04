from django.contrib import admin
from django.urls import include, path
from djangoblog import view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", view.index),
    path("post/", view.blog_posts),
    path("post/<id>", view.post),
    path("api/", include("djangoblog.api.urls")),
    path("post/add/", view.add_post),
    path("__debug__/", include("debug_toolbar.urls")),
]
