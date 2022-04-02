import requests
from django.http import HttpRequest
from django.shortcuts import render


def index(request: HttpRequest):
    return render(request, "base.html")


def post(request: HttpRequest):
    posts = requests.get("http://localhost:8000/api/v1/post").json()
    context = {"posts": posts["results"]}
    print(context)
    return render(request, "post.html", context)
