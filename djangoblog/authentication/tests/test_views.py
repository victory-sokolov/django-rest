from django.urls import reverse

from djangoblog.models import UserProfile
from djangoblog.utils.limit_test import TestCase


class TestAuth(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserProfile.objects.get(pk=1)

    def test_authenticated_user_can_see_page(self):
        self.client.force_login(user=self.user)
        response = self.client.get(reverse("get-all-posts"))
        self.assertIn(b"testuser@mail.com", response.content)

    def test_render_signup_template(self):
        response = self.client.get(reverse("signup"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "signup.html")

    def test_render_signin_template(self):
        response = self.client.get(reverse("login"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")

    def test_account_creation(self):
        pass
