from rest_framework.parsers import JSONParser
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.mixins import (
    UpdateModelMixin,
    ListModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
)
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from djangoblog.api.models import Post
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

    @extend_schema(description="Get all available blog posts")
    def get(self, request, *args, **kwargs):
        """Get all posts"""
        return self.list(request, *args, **kwargs)
        # posts = Posts.objects.all()
        # serializer = PostSerializer(posts, many=True)
        # return Response(serializer.data)

    @extend_schema(description="Create new blog post")
    def post(self, request):
        """Create post"""
        data = JSONParser().parse(request)
        serializer = PostSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
        # try:
        #     post = Posts.objects.filter(pk=id)
        #     post.delete()
        #     return Response(f"Post {id} successfully deleted!")
        # except Posts.DoesNotExist:
        #     return Response(
        #         f"Post with {id} is not found", status=status.HTTP_404_NOT_FOUND
        #     )

    def put(self, request, *args, **kwargs):
        """Update article"""
        return self.update(request, *args, **kwargs)


class SingleArticle(APIView):

    serializer_class = PostSerializer

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
