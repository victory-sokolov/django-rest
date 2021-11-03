from django.db.models import fields
from rest_framework import serializers
from djangoblog.api.models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        # fields = ["id", "user_id", "title", "body"]
        fields = "__all__"

    # def create(self, validated_data):
    #     return Posts.objects.create(validated_data)
