from rest_framework import serializers
from djangoblog.api.models.post import Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"
