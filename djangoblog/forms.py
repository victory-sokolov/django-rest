from django import forms
from tagify.fields import TagField
from django.contrib.admin.widgets import FilteredSelectMultiple
from djangoblog.api.models.post import Post, Tags
from djangoblog.models import UserProfile
from django.contrib.auth.models import Group

class PostForm(forms.ModelForm):

    tags = TagField(
        place_holder="Add a tag",
        delimiters=" ",
    )

    class Meta:
        model = Post
        exclude = ["id", "likes", "views", "favorites", "user"]

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"

        self.fields["draft"].widget.attrs["class"] = "checkbox-inline"
        self.fields["title"].widget.attrs["placeholder"] = "Blog Title"
        self.fields["slug"].widget.attrs["placeholder"] = "Blog Slug"
        self.fields["tags"].required = False

    def save(self, *args, **kwargs):
        self.tags.data_list = list(Tags.objects.all().values_list("tag", flat=True))
        super().save(*args, **kwargs)


class GroupAdminForm(forms.ModelForm):
    """GroupAdminForm."""

    class Meta:
        model = Group
        exclude = []

    users = forms.ModelMultipleChoiceField(
         queryset=UserProfile.objects.all(),
         required=False,
         widget=FilteredSelectMultiple("users", False)
    )

    def __init__(self, *args, **kwargs):
        super(GroupAdminForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["users"].initial = self.instance.user_set.all()

    def save_m2m(self):
        """Save m2m."""
        self.instance.user_set.set(self.cleaned_data['users'])

    def save(self, *args, **kwargs):
        """Save data."""
        instance = super(GroupAdminForm, self).save(commit=True)
        self.save_m2m()
        return instance
