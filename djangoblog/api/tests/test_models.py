from django.test import TestCase

from djangoblog.api.models.post import Post, Tags
from djangoblog.models import UserProfile


class TestPostModel(TestCase):

    fixtures = ["test"]

    @classmethod
    def setUpTestData(cls):
        cls.user = UserProfile.objects.get(pk=1)
        cls.post = Post.objects.create(
            user=cls.user, title="My Blog post", content="Blog post body text"
        )

    def test_post_creation(self):
        new_post = Post.objects.get(id=self.post.id)
        self.assertEquals(str(new_post), new_post.title)
        self.assertEqual(self.post.title, new_post.title)

    def test_post_has_tags(self):
        tag1 = Tags.objects.create(tag="TypeScript", slug="typescript")
        tag2 = Tags.objects.create(tag="Python", slug="python")
        self.post.tags.set([tag1, tag2])
        self.assertEqual(str(tag1), tag1.tag)
        self.assertEquals(self.post.tags.count(), 2)


class TestTags(TestCase):
    def test_add_tag_if_not_exists(self):
        tag_list = ["TypeScript", "JavaScript", "Python"]
        Tags.objects.create(tag="TypeScript", slug="typescript")
        tags = Tags.create_if_not_exist(tag_list)
        self.assertEqual(tags.count(), 3)
        self.assertEqual(Tags.objects.filter(tag="TypeScript").count(), 1)
