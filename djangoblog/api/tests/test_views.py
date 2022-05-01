from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from djangoblog.api.models.post import Post

from djangoblog.models import UserProfile


class TestPostApi(APITestCase):

    fixtures = ["test"]

    @classmethod
    def setUpTestData(cls):
        cls.user = UserProfile.objects.get(pk=1)
        cls.post = Post.objects.get(pk=1)

    def test_create_new_post(self):
        data = {
            "title": "JavaScript Fetch API",
            "body": "Fetch API Data",
            "user": self.user,
        }
        response = self.client.post("/api/v1/post/", data=data)
        self.assertEqual(201, response.status_code)
        self.assertEqual(Post.objects.count(), 2)

    def test_get_all_posts(self):
        self.client.force_login(user=self.user)
        response = self.client.get("/api/v1/post/")
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        # print(response.data)
