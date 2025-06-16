from typing import Any

from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.models import Group
from tagify.fields import TagField

from djangoblog.api.models.post import Post, Tags
from djangoblog.models import UserProfile


class PostForm(forms.ModelForm):
    tags = TagField(
        place_holder="Add a tag",
        delimiters=" ",
    )

    class Meta:
        model = Post
        fields = ["draft", "title", "slug", "content", "tags"]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"

        self.fields["draft"].widget.attrs["class"] = "checkbox-inline"
        self.fields["title"].widget.attrs["placeholder"] = "Blog Title"
        self.fields["slug"].widget.attrs["placeholder"] = "Blog Slug"
        self.fields["tags"].required = False

    def save(self, commit: bool = True, *args: list, **kwargs: dict[str, Any]) -> None:
        instance = super().save(commit=False)
        tags_data_list = Tags.objects.all().values_list("tag", flat=True)
        self.cleaned_data["tags"] = tags_data_list
        if commit:
            instance.save()
            instance.tags.clear()

        return instance


class GroupAdminForm(forms.ModelForm):
    """GroupAdminForm."""

    class Meta:
        model = Group
        exclude = []

    users = forms.ModelMultipleChoiceField(
        queryset=UserProfile.objects.all(),
        required=False,
        widget=FilteredSelectMultiple("users", False),
    )

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["users"].initial = self.instance.user_set.all()

    def save_m2m(self) -> None:
        """Save m2m."""
        self.instance.user_set.set(self.cleaned_data["users"])

    def save(self, *args: list[Any], **kwargs: dict[str, Any]) -> Group:
        """Save data."""
        instance = super().save(commit=True)
        self.save_m2m()
        return instance
