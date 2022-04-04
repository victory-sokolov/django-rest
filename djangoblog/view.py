import requests
from django.http import HttpRequest
from django.shortcuts import redirect, render

from djangoblog.forms import PostForm
from .api.models.post import Post


def index(request: HttpRequest):
    return render(request, "base.html")


def blog_posts(request: HttpRequest):
    posts = requests.get("http://localhost:8000/api/v1/post").json()
    context = {"posts": posts["results"], "form": PostForm}
    return render(request, "blog.html", context)


def post(request: HttpRequest, id: str):
    post = requests.get(f"http://localhost:8000/api/v1/post/{id}").json()
    context = {"post": post}
    return render(request, "post.html", context)


def add_post(request: HttpRequest):
    form = PostForm(request.POST)
    title = form.data["title"]
    content = form.data["post"]
    post = Post(title=title, body=content)
    post.save()
    return redirect("/post")
