import json
import logging

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, ListView

from djangoblog.api.models.post import Post, Tags
from djangoblog.forms import PostForm
from djangoblog.tasks import PostTask

logger = logging.getLogger(__name__)


class IndexView(ListView):
    template_name = "home.html"
    form_class = PostForm

    def get(self, request: HttpRequest, **kwargs) -> HttpResponse:
        context = {
            "username": request.session.get("user"),
            "form": self.form_class,
        }
        return render(request, self.template_name, context)


class SinglePostView(DetailView):
    template_name = "post.html"

    def get(self, request: HttpRequest, pk: str) -> HttpResponse:
        post = Post.objects.filter(id=pk).first()
        context = {"post": post}
        return render(request, self.template_name, context)


class PostView(ListView):
    template_name = "blog.html"
    form = PostForm

    def get(self, request: HttpRequest) -> HttpResponse:
        context = {"form": self.form, "posts": []}
        data = PostTask().apply_async()
        context["posts"] = data.get()
        return render(request, self.template_name, context)


class PostCreateView(CreateView):
    model = Post
    form_class = PostForm

    @method_decorator(login_required)
    def post(self, request: HttpRequest, **kwargs):
        is_draft = True if request.POST.get("draft") == "on" else False
        tags = json.loads(request.POST.get("tags", []))
        post = Post.objects.create(
            title=request.POST.get("title"),
            content=request.POST.get("content"),
            user=request.user,
            draft=is_draft,
        )

        tag_set = Tags.objects.create_if_not_exist(tags)
        for tag in tag_set:
            post.tags.add(tag)

        logger.info(f"New post with {post.id} has been created")
        return redirect("get-all-posts")


def handler404(request: HttpRequest, *args, **argv) -> HttpResponse:
    response = render(request, "404.html")
    response.status_code = 404
    return response
