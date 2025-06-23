import json
from uuid import uuid4

from django.urls import reverse
from rest_framework.test import APIClient

from djangoblog.api.models.post import Post
from djangoblog.factory import AccountFactory
from djangoblog.forms import PostForm
from djangoblog.models import UserProfile
from djangoblog.utils.limit_test import TestCase


class HomePageTest(TestCase):
    def test_home_page_status_code(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_by_name(self):
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
        cls.factory = AccountFactory()
        cls.user = UserProfile.objects.create(
            name="TestUser",
            email=cls.factory.user.email,
            password=cls.factory.user.password,
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
            slug="test-post",
            user=self.user,
        )
        response = self.api_client.get(
            reverse("get-post-by-id", kwargs={"pk": str(post.id)}),
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Test post data", str(response.content))
        self.assertTemplateUsed(response, "post.html")

    def test_add_post_form_submitted(self):
        self.client.force_login(user=self.user)
        form_data = {
            "title": "Post Title",
            "content": "Post body",
            "slug": str(uuid4()),
            "tags": json.dumps(
                [
                    {"value": "Python", "slug": "python"},
                    {"value": "Django", "slug": "django"},
                ],
            ),
        }
        form = PostForm(form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_invalid_form_validation_fails(self):
        self.client.force_login(user=self.user)
        form = PostForm(data={})
        self.assertFalse(form.is_valid())
