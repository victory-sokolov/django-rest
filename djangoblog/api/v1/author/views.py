from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.parsers import JSONParser
from rest_framework.request import Request
from rest_framework.response import Response
from djangoblog.api.models.author import Author
from djangoblog.api.v1.author.serializers import AuthorSerializer
from rest_framework.viewsets import GenericViewSet


@extend_schema(tags=["author"])
class AuthorView(
    GenericViewSet,
    UpdateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
    CreateModelMixin,
):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    @extend_schema(operation_id="Author", description="Get all authors")
    def get(self, request: Request):
        return self.list(request)

    @extend_schema(description="Add new author")
    def post(self, request: Request):
        """Add new author"""
        data = JSONParser().parse(request)
        serializer = AuthorSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, pk: int):
        """Delete author"""
        return self.destroy(request, pk)

    def put(self, request: Request, pk: int):
        """Update author details"""
        return self.update(request, pk)

    def retrieve(self, request, pk: int):
        """Get author by id"""
        try:
            post = Author.objects.get(pk=pk)
        except Author.DoesNotExist:

            return Response(
                f"Post with id: '{pk}' is not found", status=status.HTTP_400_BAD_REQUEST
            )

        # serializer = Author(post)
        return Response(post.data)
