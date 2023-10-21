import logging
from django.contrib import admin

from django.conf import settings
from django.contrib.auth.models import Permission
from django.contrib.auth.models import Group
from django.http import HttpRequest

from djangoblog.forms import GroupAdminForm
from djangoblog.api.models.post import Post
from djangoblog.forms import PostForm
from djangoblog.models import UserProfile

logger = logging.getLogger(__name__)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "user",
        "likes",
    )
    filter_horizontal = ("permissions",)
    readonly_fields = ["id", "user"]
    list_filter = (
        "created_at",
        "likes",
    )
    search_fields = ["title"]
    exclude = ("likes", "views", "favorites")
    ordering = ("-user", "title")

    form = PostForm


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
    )

    @admin.action(description="Total posts")
    def get_total_posts(self, obj):
        return obj.post_set.count()

    def get_readonly_fields(self, request: HttpRequest, obj):
        if request.user.is_superuser:
            return ("is_active", "is_staff", "is_superuser",)

        return super().get_readonly_fields(request, obj)

    # def save_model(self, request, obj: UserProfile, form, change):
    #     permissions = Permission.objects.filter(codename__in=settings.STAFF_PERMISSIONS)
    #     obj.user_permissions.add(*permissions)
    #     logger.info(f"Permissions {list(permissions)} added for user {obj.email}")
    #     super().save_model(request, obj, form, change)


class GroupAdmin(admin.ModelAdmin):

    form = GroupAdminForm
    filter_horizontal = ["permissions"]


admin.site.unregister(Group)

admin.site.register(Group, GroupAdmin)
