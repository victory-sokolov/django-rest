import secrets
from datetime import datetime, timedelta

from django.utils import timezone
from factory import Faker, LazyAttribute, lazy_attribute
from factory.django import DjangoModelFactory

from djangoblog.api.models.post import Post
from djangoblog.models import UserProfile
from djangoblog.utilities import slugify


class AccountFactory(DjangoModelFactory):
    class Meta:
        model = Post

    title = Faker("sentence", nb_words=15)
    content = Faker("sentence", nb_words=10000)
    slug = LazyAttribute(lambda obj: slugify(obj.title))

    @lazy_attribute
    def user(self) -> UserProfile:
        return self.get_default_user()

    @lazy_attribute
    def created_at(self) -> datetime:
        days = secrets.randbelow(61)
        dt = datetime.now() - timedelta(days=days)
        return timezone.make_aware(dt)

    @classmethod
    def get_default_user(cls) -> UserProfile:
        """Get or create the default user for posts."""
        from faker import Faker as StandaloneFaker

        fake = StandaloneFaker()
        user, _ = UserProfile.objects.get_or_create(
            email="admin@gmail.com",
            defaults={
                "email": "admin@gmail.com",
                "name": "Admin",
                "password": fake.password(length=10),
            },
        )
        return user

    @classmethod
    def create_bulk(cls, count: int) -> list[Post]:
        """Create posts using bulk_create for optimal performance."""
        from faker import Faker

        fake = Faker()
        user = cls.get_default_user()

        posts = []
        for _ in range(count):
            title = fake.sentence(nb_words=15)
            days = secrets.randbelow(61)
            dt = datetime.now() - timedelta(days=days)
            created_at = timezone.make_aware(dt)

            post = Post(
                user=user,
                title=title,
                content=fake.sentence(nb_words=10000),
                slug=slugify(title),
                created_at=created_at,
            )
            posts.append(post)

        return Post.objects.bulk_create(posts)
