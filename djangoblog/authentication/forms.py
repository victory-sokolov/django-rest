from django import forms

from djangoblog.models import UserProfile


class SignUpForm(forms.Form):
    name = forms.CharField(
        label="Name",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "name": "name",
                "id": "name",
                "placeholder": "Name",
            },
        ),
    )
    email = forms.CharField(
        label="Email",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "name": "email",
                "id": "email",
                "placeholder": "Email",
            },
        ),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "name": "password",
                "id": "password",
                "placeholder": "Password",
            },
        ),
    )

    class Meta:
        model = UserProfile


class LoginForm(SignUpForm):
    name = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update(
            {
                "id": "login-email",
                "placeholder": "Email",
            },
        )
        self.fields["password"].widget.attrs.update(
            {
                "id": "login-password",
                "placeholder": "Password",
            },
        )
