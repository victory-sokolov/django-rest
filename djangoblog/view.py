import requests
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from djangoblog.api.models.post import Post
from djangoblog.forms import PostForm


def index(request: HttpRequest):
    context = {"username": request.session.get("user")}
    return render(request, "home.html", context)


@login_required(login_url="login")
def blog_posts(request: HttpRequest):
    posts = requests.get("http://localhost:8000/api/v1/post").json()
    context = {"posts": posts["results"], "form": PostForm}
    return render(request, "blog.html", context)


def post(request: HttpRequest, id: str):
    post = requests.get(f"http://localhost:8000/api/v1/post/{id}").json()
    context = {"post": post}
    return render(request, "post.html", context)


@login_required
def add_post(request: HttpRequest):

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            is_draft = True if form.data.get("draft") == "on" else False
            post = Post(
                title=form.data["title"],
                body=form.data["post"],
                user=request.user,
                draft=is_draft,
            )
            post.save()
            return redirect("post")
    else:
        form = PostForm()

    return render(request, "post.html", {"form": form})
