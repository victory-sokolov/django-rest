from django.urls import path
from djangoblog.authentication import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("login/", views.login_user, name="login"),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="login.html"),
        name="logout",
    ),
]
