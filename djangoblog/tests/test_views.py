from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from rest_framework.test import APIClient

from djangoblog.api.models.post import Post
from djangoblog.forms import PostForm
from djangoblog.models import UserProfile


class HomePageTest(SimpleTestCase):
    def test_home_page_status_code(self):
        response = self.client.get("/")
        self.assertEquals(response.status_code, 200)

    def tet_view_url_by_name(self):
        response = self.client.get(reverse("home"))
        self.assertEquals(response.status_code, 200)

    def test_template_render(self):
        response = self.client.get(reverse("home"))
        self.assertEquals(response.status_code, 200)
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

    def test_blog_template_render(self):
        response = self.client.get(reverse("post"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "blog.html")

    def test_post_render(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        post = Post.objects.create(
            title="Test post",
            body="Test post data",
            user=self.user,
        )
        response = client.get(reverse("post", kwargs={"id": str(post.id)}))

    def test_render_post_template(self):
        self.client.force_login(user=self.user)
        response = self.client.get(reverse("add_post"))
        self.assertTemplateUsed(response, "post.html")

    def test_add_post(self):
        self.client.force_login(user=self.user)
        form_data = {
            "title": "Post Title",
            "post": "Post body",
            "tags": ["Python", "Js"],
        }
        self.client.post(reverse("add_post"), data=form_data)
        form = PostForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        self.client.force_login(user=self.user)
        self.client.post(reverse("add_post"), data={})
        form = PostForm(data={})
        self.assertFalse(form.is_valid())
