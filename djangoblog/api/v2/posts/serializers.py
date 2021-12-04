from rest_framework import serializers
from djangoblog.api.models.post import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        # fields = ["id", "user_id", "title", "body"]
        fields = "__all__"
