from django.contrib import admin
from djangoblog.api.models.post import Post
from djangoblog.models import UserProfile


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "likes")
    list_filter = ("created_at",)
    search_fields = ["title"]
    exclude = ("likes", "views", "favorites")
    ordering = ("-user", "title")


@admin.register(UserProfile)
class UserAdmin(admin.ModelAdmin):

    list_display = ("email", "name", "get_total_posts")
    fieldsets = (
        (
            "Personal info",
            {
                "fields": (
                    "email",
                    "name",
                    "password",
                    "profile_picture",
                )
            },
        ),
        (
            ("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    def get_total_posts(self, obj):
        return obj.post_set.count()

    get_total_posts.short_description = "Total posts"
