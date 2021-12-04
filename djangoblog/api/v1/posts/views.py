from django.contrib.auth import authenticate
from rest_framework.parsers import JSONParser
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.mixins import (
    UpdateModelMixin,
    ListModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
)
from rest_framework.views import APIView
from rest_framework.authentication import (
    BasicAuthentication,
    SessionAuthentication,
    TokenAuthentication,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from drf_spectacular.utils import extend_schema

from djangoblog.api.models.post import Post
from djangoblog.api.v1.posts.serializers import PostSerializer

class ArticleView(
    generics.GenericAPIView,
    UpdateModelMixin,
    ListModelMixin,
    DestroyModelMixin,
    CreateModelMixin,
):

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(description="Get all available blog posts")
    def get(self, request: Request, *args, **kwargs):
        """Get all posts"""
        return self.list(request, *args, **kwargs)

    @extend_schema(description="Create new blog post")
    def post(self, request: Request):
        """Create post"""
        data = JSONParser().parse(request)
        serializer = PostSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def put(self, request: Request, *args, **kwargs):
        """Update article"""
        return self.update(request, *args, **kwargs)


class SingleArticle(APIView):

    serializer_class = PostSerializer
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk: int):
        """Get single article by id"""
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:

            return Response(
                f"Post with id: '{pk}' is not found", status=status.HTTP_400_BAD_REQUEST
            )

        serializer = PostSerializer(post)
        return Response(serializer.data)
