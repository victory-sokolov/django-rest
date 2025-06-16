from drf_spectacular.utils import extend_schema_serializer
from rest_framework import serializers

from djangoblog.api.models.post import Post, Tags
from djangoblog.api.v1.posts.validators import SlugValidator, TagValidator


class PostStatistics(serializers.ModelSerializer):
    class Meta:
        model = Post
        read_only_fields = ["likes", "favorites", "views"]


class TagSerializer(serializers.ModelSerializer):
    value = serializers.CharField(min_length=3)
    slug = serializers.CharField(min_length=3)

    class Meta:
        model = Tags
        fields = ["value", "slug"]
        validators = [TagValidator()]
        read_only_fields = []


@extend_schema_serializer(exclude_fields=("title", "content", "user"))
class PostSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    title = serializers.CharField(required=True)
    slug = serializers.CharField(
        max_length=100,
        required=False,
        validators=[SlugValidator()],
    )
    content = serializers.CharField(required=True)
    tags = TagSerializer(many=True, required=False)

    def create(self, validated_data: dict) -> Post:
        user = self.context["request"].user
        tags_data = validated_data.pop("tags", [])
        post, _ = Post.objects.update_or_create(
            user=user,
            id=self.context.get("post_id"),
            defaults=validated_data,
        )

        for tag_data in tags_data:
            tag, _ = Tags.objects.get_or_create(tag=tag_data["tag"])
            post.tags.add(tag)
        return post

    def update(self, instance: Post, validated_data: dict) -> Post:
        # extract the tags data from validated_data
        tags_data = validated_data.pop("tags", None)
        if tags_data is not None:
            # remove the old tags and add the new tags to the post instance
            instance.tags.clear()
            for tag_data in tags_data:
                tag, _ = Tags.objects.get_or_create(tag=tag_data["tag"])
                instance.tags.add(tag)

        return super().update(instance, validated_data)

    class Meta:
        model = Post
        fields = ["id", "title", "slug", "user", "tags", "content"]
        read_only_fields = ["user", "tags"]
