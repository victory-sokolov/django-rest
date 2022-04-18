from django.db.models.query import QuerySet
from django.db.models.query_utils import Q
import requests

from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from djangoblog.api.models.post import Post, Tags
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
            tags = form.data.get("tags", "").split(" ")

            post = Post.objects.create(
                title=form.data["title"],
                body=form.data["post"],
                user=request.user,
                draft=is_draft,
            )
            tags_obj = Tags.objects.filter(tag__in=tags)
            if not tags_obj.exists():
                for t in tags_obj:
                    Tags.objects.create(tag=t, slug=t.lower().replace(" ", "-"))
                    post.tag.add(t)
                # Tags.objects.bulk_create(
                #     Tags(tag=t, slug=t.lower().replace(" ", "-")) for t in tags
                # )

            return redirect("post")

    return render(request, "post.html")
