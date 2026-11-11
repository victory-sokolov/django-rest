from django.test import TestCase

from djangoblog.factory import AccountFactory
from djangoblog.models import UserProfile


class AccountFactoryTests(TestCase):
    def test_default_user_is_created_and_reused(self):
        first = AccountFactory(title="First", content="Content")
        second = AccountFactory(title="Second", content="Content")

        self.assertEqual(first.user.email, "admin@gmail.com")
        self.assertEqual(first.user, second.user)
        self.assertEqual(UserProfile.objects.filter(email="admin@gmail.com").count(), 1)

    def test_explicit_user_is_respected(self):
        user = UserProfile.objects.create(email="other@example.com", name="Other")

        post = AccountFactory(title="Post", content="Content", user=user)

        self.assertEqual(post.user, user)
        self.assertFalse(UserProfile.objects.filter(email="admin@gmail.com").exists())
