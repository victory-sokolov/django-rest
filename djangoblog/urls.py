from django.contrib import admin
from django.urls import include, path
from djangoblog import settings, view
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", view.index, name="home"),
    path("post/", view.blog_posts, name="post"),
    path("post/<id>", view.post),
    path("post/add/", view.add_post, name="add_post"),
    path("api/", include("djangoblog.api.urls"), name="api"),
    path("auth/", include("djangoblog.authentication.urls"), name="auth"),
    path("__debug__/", include("debug_toolbar.urls")),
    path("ckeditor/", include("ckeditor_uploader.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
