from typing import Union

from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from djangoblog.api.models.post import Post, Tags
from djangoblog.api.v1.posts.serializers import PostSerializer
from djangoblog.forms import PostForm
from djangoblog.tasks import retrieve_all_posts


def index(request: HttpRequest):
    context = {"username": request.session.get("user"), "form": PostForm}
    return render(request, "home.html", context)


def post(request: HttpRequest, id: Union[str, None] = None):
    """Get all or single post by id."""
    context = {"form": PostForm, "posts": []}
    if id:
        post = Post.objects.filter(id=id).first()
        context["post"] = post
        return render(request, "post.html", context)

    data = retrieve_all_posts.delay()
    context["posts"] = data.get()
    return render(request, "blog.html", context)


@login_required
def add_post(request: HttpRequest):
    """Add new post."""
    if request.method == "POST":
        form = PostForm(request.POST)

        if form.is_valid():
            is_draft = True if form.data.get("draft") == "on" else False
            tags = form.data.get("tags", "").split(" ")
            post = Post.objects.create(
                title=form.data["title"],
                content=form.data["post"],
                user=request.user,
                draft=is_draft,
            )

            tag_set = Tags.objects.create_if_not_exist(tags)
            for tag in tag_set:
                post.tags.add(tag)
            return redirect("post")

    return render(request, "post.html")


def handler404(request: HttpRequest, *args, **argv):
    response = render(request, "404.html")
    response.status_code = 404
    return response
