from django.contrib import admin
from djangoblog.api.models.post import Post, Author, Category
from djangoblog.models import UserProfile

models = [Post, Author, Category, UserProfile]
admin.site.register(models)
