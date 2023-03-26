from djangoblog.api.v1.posts.validators import TagValidator, TitleValidator, SlugValidator
from drf_spectacular.utils import extend_schema_serializer
from rest_framework import serializers
from djangoblog.api.models.post import Post, Tags

class PostStatistics(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["likes", "favorites", "views"]


class TagSerializer(serializers.ModelSerializer):

    tag = serializers.CharField(min_length=3)

    class Meta:
        model = Tags
        fields = ["tag"]
        validators=[TagValidator()]


@extend_schema_serializer(exclude_fields=("title", "content", "user"))
class PostSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field="name", read_only=True)
    title = serializers.CharField(required=True, validators=[TitleValidator()])
    slug = serializers.CharField(max_length=100, required=False, validators=[SlugValidator()])
    content = serializers.CharField(required=True)
    tags = TagSerializer(many=True, required=False)
    
    def create(self, validated_data):
        user = self.context["request"].user
        tags_data = validated_data.pop('tags', [])
        post, _ = Post.objects.update_or_create(
            user=user, id=self.context.get("post_id"), defaults=validated_data
        )

        for tag_data in tags_data:
            tag, _ = Tags.objects.get_or_create(tag=tag_data['tag'])
            post.tags.add(tag)
        return post


    class Meta:
        model = Post
        fields = ["title", "slug", "tags", "user", "content"]
