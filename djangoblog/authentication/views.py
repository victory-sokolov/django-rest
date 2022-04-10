import logging

from django.http import HttpRequest
from django.shortcuts import redirect, render
from djangoblog.authentication.forms import SignUpForm, LoginForm
from djangoblog.models import UserProfile
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.utils.safestring import mark_safe

from django.contrib.auth import authenticate, login

logger = logging.getLogger(__name__)


def signup(request: HttpRequest):

    if "user" in request.session:
        return redirect("home")

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():

            user = UserProfile(
                name=form.cleaned_data.get("name"),
                email=form.cleaned_data.get("email"),
                password=make_password(form.cleaned_data.get("password")),
            )
            user.save()
            messages.success(
                request,
                mark_safe(
                    "Account successfully created. \n You can <a href='/auth/login/'>Log In</a>"
                ),
            )
            return redirect("signup")

    form = SignUpForm()
    return render(request, "signup.html", {"form": form})


def login_user(request: HttpRequest):

    if "user" in request.session:
        return redirect("home")

    if request.method == "POST":
        form = LoginForm(request.POST)
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(email=email, password=password)

        if user is None:
            messages.error(request, "Invalid Credentials")
            return redirect("login")

        request.session["user"] = email
        login(request, user)
        return redirect("home")

    form = LoginForm()
    return render(request, "login.html", {"form": form})
