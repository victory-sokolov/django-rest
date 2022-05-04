from drf_spectacular.utils import extend_schema_serializer
from rest_framework import serializers
from djangoblog.api.models.post import Post, Tags


class PostStatistics(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["likes", "favorites", "views"]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = "__all__"


@extend_schema_serializer(exclude_fields=("title", "content", "created_at"))
class PostSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field="name", read_only=True)
    tags = TagSerializer(many=True, required=False)
    statistics = PostStatistics(source="*", read_only=True, required=False)

    def create(self, validated_data):
        user = self.context["request"].user
        post, created = Post.objects.update_or_create(
            user=user, id=self.context.get("post_id"), defaults=validated_data
        )
        return post

    class Meta:
        model = Post
        exclude = ["views", "likes", "favorites"]
