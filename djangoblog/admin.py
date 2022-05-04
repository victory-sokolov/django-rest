from django.contrib import admin
from djangoblog.api.models.post import Post
from djangoblog.models import UserProfile


class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "likes")
    list_filter = ("created_at",)
    search_fields = ["title"]


models = [UserProfile]

admin.site.register(models)
admin.site.register(Post, PostAdmin)
