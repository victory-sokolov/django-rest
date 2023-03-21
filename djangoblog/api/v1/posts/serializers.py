from djangoblog.api.v1.posts.validators import TitleValidator, SlugsValidator
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
    title = serializers.CharField(validators=[TitleValidator()])
    slug = serializers.CharField(max_length=100, required=False, validators=[SlugsValidator()])
    tags = TagSerializer(many=True, required=False)
    statistics = PostStatistics(source="*", read_only=True, required=False)
    
    # def create(self, validated_data):
    #     user = self.context["request"].user
    #     post, created = Post.objects.update_or_create(
    #         user=user, id=self.context.get("post_id"), defaults=validated_data
    #     )
    #     return post

    # def validate(self, attrs):
    #     validated_data = super().validate(attrs)
    #     return SlugsValidator()(validated_data['slug'], validated_data['title'])
    
    class Meta:
        model = Post
        # validators=[TitleValidator(), SlugsValidator()]
        fields = ["title", "slug", "statistics", "tags", "user"]
