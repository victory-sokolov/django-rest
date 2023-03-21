from django.urls import path
from djangoblog.authentication import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("login/", views.LoginView.as_view(), name="login"),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="login.html"),
        name="logout",
    ),
]
