from django import forms


class PostForm(forms.Form):
    title = forms.CharField(
        label="Article Title",
        widget=forms.TextInput(attrs={"class": "form-control", "id": "title"}),
    )
    post = forms.CharField(
        label="Content",
        widget=forms.Textarea(
            attrs={"class": "form-control", "rows": "5", "id": "content"}
        ),
    )
