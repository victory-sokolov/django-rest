import json
from uuid import uuid4

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from djangoblog.api.models.post import Post
from djangoblog.models import UserProfile


class TestPostApi(APITestCase):
    fixtures = ["test"]

    @classmethod
    def setUpTestData(cls):
        cls.user = UserProfile.objects.get(pk=1)
        cls.post = Post.objects.get(pk=1)

    def setUp(self):
        self.client.force_login(user=self.user)

    def test_create_new_post(self):
        data = {"title": "JavaScript Fetch API", "content": "Fetch API Data"}
        response = self.client.post("/api/v1/post/", data=data)
        self.assertEqual(201, response.status_code)
        self.assertEqual(Post.objects.count(), 2)

    def test_get_all_posts(self):
        response = self.client.get("/api/v1/post/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_post_bad_request(self):
        data = {"title": "JavaScript Fetch API", "content": "Fetch API Data"}
        response = self.client.post("/api/v1/post/", data=data)
        post_id = json.loads(response.content)["id"]

        response = self.client.post("/api/v1/post/", data={})
        response2 = self.client.put(f"/api/v1/post/{post_id}/", data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_post(self):
        data = {"title": "JavaScript Fetch API", "content": "Fetch API Data"}
        post = self.client.post("/api/v1/post/", data=data)
        id = json.loads(post.content)["id"]
        response = self.client.delete(f"/api/v1/post/{id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_not_found(self):
        data = {"title": "Title 2", "content": "Content 2"}
        update_post = self.client.put(f"/api/v1/post/{uuid4()}/", data=data)
        delete_post = self.client.delete(f"/api/v1/post/{uuid4()}/")
        get_post = self.client.get(f"/api/v1/post/{uuid4()}/")

        self.assertEqual(update_post.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(delete_post.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(get_post.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_post(self):
        initial_data = {"title": "JavaScript Fetch", "content": "Fetch Data"}
        new_data = {"title": "JavaScript Axios", "content": "Axios Data"}
        create_post = self.client.post(
            "/api/v1/post/",
            data=initial_data,
        ).content
        post = json.loads(create_post)

        response = self.client.put(
            f"/api/v1/post/{post['id']}/",
            data=new_data,
        )
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), "JavaScript Axios")
        self.assertEqual(data.get("content"), "Axios Data")


class TestTokenApi(APITestCase):
    fixtures = ["test"]

    @classmethod
    def setUpTestData(cls):
        cls.user = UserProfile.objects.get(pk=1)
        cls.api_client = APIClient()

    def test_token_success(self):
        url = reverse("token_obtain_pair")
        self.api_client.force_authenticate(user=self.user)
        credentials = {
            "email": self.user.email,
            "password": self.user.password,
        }
        user = UserProfile.objects.create(
            email="nick@test.com",
            password="1234567",
            name="Nick",
        )
        self.api_client.credentials(
            email=self.user.email,
            password=self.user.password,
        )
        self.api_client.login(email="nick@test.com", password="1234567")
        response = self.api_client.post(url, data=credentials)
