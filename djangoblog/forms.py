from django import forms
from ckeditor.widgets import CKEditorWidget


class PostForm(forms.Form):
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "title",
                "placeholder": "Article Title",
            }
        ),
    )
    post = forms.CharField(
        widget=CKEditorWidget(
            attrs={"class": "form-control", "rows": "5", "id": "content"}
        ),
    )
    draft = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "checkbox-inline", "id": "draft"}),
    )
