from django import forms
from ckeditor.widgets import CKEditorWidget


class PostForm(forms.Form):
    title = forms.CharField(
        label="Article Title",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "title",
                "placeholder": "Article Title",
            }
        ),
    )
    post = forms.CharField(
        label="Content",
        widget=CKEditorWidget(
            attrs={
                "class": "form-control",
                "rows": "5",
                "id": "content"
            }
        ),
    )
