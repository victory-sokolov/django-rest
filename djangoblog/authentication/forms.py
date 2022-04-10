from django import forms

from djangoblog.models import UserProfile


class SignUpForm(forms.Form):
    name = forms.CharField(
        label="Name",
        widget=forms.TextInput(
            attrs={"class": "form-control", "id": "name", "placeholder": "Name"}
        ),
    )
    email = forms.CharField(
        label="Email",
        widget=forms.EmailInput(
            attrs={"class": "form-control", "id": "email", "placeholder": "Email"}
        ),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "id": "password", "placeholder": "Password"}
        ),
    )

    class Meta:
        model = UserProfile


class LoginForm(SignUpForm):
    name = None
