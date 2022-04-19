from typing import Union
import requests

from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from djangoblog.api.models.post import Post, Tags
from djangoblog.forms import PostForm


def index(request: HttpRequest):
    context = {"username": request.session.get("user"), "form": PostForm}
    return render(request, "home.html", context)


def post(request: HttpRequest, id: Union[str, None] = None):
    context = {"form": PostForm}
    if id:
        post = requests.get(f"http://localhost:8000/api/v1/post/{id}").json()
        context["post"] = post
        return render(request, "post.html", context)

    posts = requests.get("http://localhost:8000/api/v1/post").json()
    context["posts"] = posts["results"]
    return render(request, "blog.html", context)

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

            return redirect("post")
        
    return render(request, "post.html")
