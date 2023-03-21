from django.test import SimpleTestCase, TestCase, Client
from django.urls import reverse

from rest_framework.test import APIClient, APITestCase

from djangoblog.api.models.post import Post
from djangoblog.forms import PostForm
from djangoblog.models import UserProfile


class HomePageTest(SimpleTestCase):
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
        response = self.client.get(reverse("post"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog.html")

    def test_single_post_rendered(self):
        self.api_client.force_authenticate(user=self.user)
        post = Post.objects.create(
            title="Test post",
            content="Test post data",
            user=self.user,
        )
        self.api_client.get(reverse("post", kwargs={"id": str(post.id)}))
        response = self.client.get(reverse("post"))
        self.assertEqual(response.status_code, 200)
        # self.assertIn("Test post data", str(response.content))

    def test_render_post_template(self):
        self.client.force_login(user=self.user)
        response = self.client.get(reverse("add_post"))
        self.assertTemplateUsed(response, "post.html")

    def test_add_post(self):
        self.client.force_login(user=self.user)
        form_data = {"title": "Post Title", "post": "Post body"}
        response = self.client.post(reverse("add_post"), data=form_data, format="json")
        # print(response)
        # form = PostForm(data=form_data)
        # self.assertTrue(form.is_valid())
        # response = self.api_client.get(reverse("post"))
        # print(response.data)
        # self.assertIn("Post body", str(response.content))

    def test_invalid_form(self):
        self.client.force_login(user=self.user)
        self.client.post(reverse("add_post"), data={})
        form = PostForm(data={})
        # self.assertFalse(form.is_valid())
