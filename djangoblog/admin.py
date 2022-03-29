from django.contrib import admin
from djangoblog.api.models.post import Post, Author, Category

models = [Post, Author, Category]
admin.site.register(models)
