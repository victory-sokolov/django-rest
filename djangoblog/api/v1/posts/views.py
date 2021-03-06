from django.http import Http404
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from drf_spectacular.utils import extend_schema

from djangoblog.api.models.post import Post
from djangoblog.api.v1.posts.serializers import PostSerializer

from rest_framework.permissions import IsAuthenticated


@extend_schema(tags=["post"])
class ArticleListView(APIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(description="Get all available blog posts")
    def get(self, request: Request):
        """Get all posts"""
        post = Post.objects.filter(draft=False).order_by("-created_at")
        serializer = PostSerializer(post, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @extend_schema(description="Create new blog post", tags=["post"])
    def post(self, request: Request):
        """Create post"""
        context = {"request": request}
        serializer = PostSerializer(data=request.data, context=context)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["post"])
class SingleArticleView(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, user_id: int, post_id=None):
        try:
            if user_id:
                return Post.objects.filter(user_id=user_id, id=post_id, draft=False)
            return Post.objects.filter(draft=False)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request: Request, id: str):
        """Get single article."""
        post = Post.objects.filter(id=id).first()
        if not post:
            return Response(
                {"response": f"Post with id {id} doesn't exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = PostSerializer(post)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def delete(self, request: Request, id: str):
        """Delete post by id"""
        post = self.get_object(request.user.id, id)
        if not post:
            return Response(
                {"response": f"Post with id {id} doesn't exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        post.delete()
        return Response(
            {"response": f"Post with id {id} has been deleted."},
            status=status.HTTP_200_OK,
        )

    def put(self, request: Request, id: str):
        """Update article"""
        post = self.get_object(request.user.id, id)
        if not post:
            return Response(
                {"response": f"Post with id {id} doesn't exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        context = {"request": request, "post_id": id}
        serializer = PostSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
