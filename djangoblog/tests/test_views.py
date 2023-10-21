import json
from django.test import SimpleTestCase, TestCase, Client
from django.urls import reverse

from rest_framework.test import APIClient, APITestCase

from djangoblog.api.models.post import Post
from djangoblog.forms import PostForm
from djangoblog.models import UserProfile


class HomePageTest(TestCase):
    def test_home_page_status_code(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def tet_view_url_by_name(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_template_render(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")

    def test_home_contains_correct_html(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"You have to", response.content)


class BlogPageTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserProfile.objects.create(
            name="TestUser", email="test@gmail.com", password="pass"
        )
        cls.api_client = APIClient()

    def test_blog_template_render(self):
        response = self.client.get(reverse("get-all-posts"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog.html")

    def test_single_post_rendered(self):
        self.api_client.force_authenticate(user=self.user)
        post = Post.objects.create(
            title="Test post",
            content="Test post data",
            user=self.user,
        )
        response = self.api_client.get(
            reverse("get-post-by-id", kwargs={"pk": str(post.id)}))
        self.assertEqual(response.status_code, 200)
        self.assertIn("Test post data", str(response.content))
        self.assertTemplateUsed(response, "post.html")

    def test_add_post(self):
        self.client.force_login(user=self.user)
        form_data = {
            "title": "Post Title",
            "post": "Post body",
            "tags": json.dumps([{'value': 'Python'}, {'value': 'Django'}]),
        }
        response = self.client.post(
            reverse("create-post"),
            data=form_data,
            follow=True,
        )
        self.assertEqual(response.status_code, 200)

    def test_invalid_form(self):
        self.client.force_login(user=self.user)
        form = PostForm(data={})
        self.assertFalse(form.is_valid())
