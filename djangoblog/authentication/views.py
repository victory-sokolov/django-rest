import logging
from html import escape

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from django.http import (
    HttpResponse,
    HttpResponsePermanentRedirect,
    HttpResponseRedirect,
)
from django.shortcuts import redirect, render
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.http import HttpRequest

from djangoblog.authentication.forms import LoginForm, SignUpForm
from djangoblog.models import UserProfile

logger = logging.getLogger(__name__)


class LoginView(FormView):
    form_class = LoginForm
    template_name = "login.html"

    def post(
        self,
        request: HttpRequest,
    ) -> HttpResponseRedirect | HttpResponsePermanentRedirect:
        if "user" in request.session:
            return redirect("home")

        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)

        if not user:
            messages.error(request, "Invalid Credentials")
            return redirect("login")

        request.session["user"] = email
        logger.info(f"User {email} has successfully logged in")
        login(request, user)
        return redirect("home")


class SignUpView(ListView):
    form = SignUpForm()
    model = UserProfile
    template_name = "signup.html"

    def get(self, request: HttpRequest) -> HttpResponseRedirect | HttpResponse:
        if "user" in request.session:
            return redirect("home")

        return render(request, "signup.html", {"form": self.form})

    def post(self, request: HttpRequest) -> HttpResponseRedirect | HttpResponse:
        form = SignUpForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data.get("name")
            email = form.cleaned_data.get("email")
            try:
                user = UserProfile(
                    name=name,
                    email=email,
                    password=make_password(form.cleaned_data.get("password")),
                )
                user.save()
            except IntegrityError:
                logger.warning(f"User with {email} already exists")
                messages.warning(
                    request,
                    escape(f"User {email} already exists"),
                )
                return redirect("signup")

            messages.success(
                request,
                escape(
                    "Account successfully created. \n You can <a href='/auth/login/'>Log In</a>",
                ),
            )
            logger.info(f"User with id: {user.id} successfully created.")
            return redirect("signup")

        return render(request, "signup.html", {"form": form})
