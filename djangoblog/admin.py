from django.contrib import admin
from djangoblog.api.models.post import Post, Category
from djangoblog.models import UserProfile

models = [Post, Category, UserProfile]
admin.site.register(models)
