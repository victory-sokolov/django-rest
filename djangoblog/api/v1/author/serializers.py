from django.db import models
from django.db.models import fields
from rest_framework import serializers
from djangoblog.api.models.post import Author


class AuthorSerializer(serializers.ModelSerializers):
    class Meta:
        model = Author
        fields = "__all__"
