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

    user = UserProfile.objects.get_or_create(
        email="admin@gmail.com",
        defaults={
            "email": "admin@gmail.com",
            "name": "Admin",
            "password": Faker("password", length=10),
        },
    )[0]
    title = Faker("sentence", nb_words=15)
    content = Faker("sentence", nb_words=10000)
    slug = LazyAttribute(lambda obj: slugify(obj.title))

    @lazy_attribute
    def created_at(self) -> datetime:
        days = secrets.randbelow(61)
        dt = datetime.now() - timedelta(days=days)
        return timezone.make_aware(dt)
