from drf_spectacular.utils import extend_schema_serializer
from rest_framework import serializers
from djangoblog.api.models.category import Category
from djangoblog.api.models.post import Post
from djangoblog.models import UserProfile

class ArticleSerializer(serializers.Serializer):
    title = serializers.CharField()
    content = serializers.CharField()
    created_at = serializers.CharField()


@extend_schema_serializer(exclude_fields=("title", "body", "created_at"))
class PostSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        many=True, slug_field="category", queryset=Category.objects.all()
    )
    user = serializers.SlugRelatedField(
        slug_field="name", queryset=UserProfile.objects.all()
    )
    article = ArticleSerializer(many=True, read_only=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        cat = data.pop("category")
        title = data.pop("title")
        content = data.pop("body")
        created_at = data.pop("created_at")
        data["categories"] = cat
        data["article"] = {"title": title, "content": content, "created_at": created_at}
        return data

    class Meta:
        model = Post
        fields = "__all__"
