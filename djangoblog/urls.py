from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from djangoblog import view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", view.IndexView.as_view(), name="home"),
    path("post/", view.PostView.as_view(), name="get-all-posts"),
    path("post/<pk>", view.SinglePostView.as_view(), name="get-post-by-id"),
    path("post/add/", view.PostCreateView.as_view(), name="create-post"),
    path("api/", include("djangoblog.api.urls"), name="api"),
    path("auth/", include("djangoblog.authentication.urls"), name="auth"),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path(
        "admin/password_reset/",
        auth_views.PasswordResetView.as_view(),
        name="admin_password_reset",
    ),
    path(
        "admin/password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path("health/app", view.healthcheck, name="App Health check"),
    path("health/db/", view.db_health_check, name="Database Health check"),
    path("", include("django_prometheus.urls")),
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT,
)

if settings.DEBUG:
    urlpatterns += [
        path("silk/", include("silk.urls", namespace="silk")),
        path("__debug__/", include("debug_toolbar.urls")),
    ]

handler404 = "djangoblog.view.handler404"
