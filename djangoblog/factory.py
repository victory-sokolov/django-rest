import secrets
from datetime import datetime, timedelta

import factory
from django.utils import timezone

from djangoblog.api.models.post import Post
from djangoblog.models import UserProfile


class AccountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    user = UserProfile.objects.get_or_create(
        email="admin@gmail.com",
        defaults={
            "email": "admin@gmail.com",
            "name": "Admin",
            "password": factory.Faker("password", length=10),
        },
    )[0]
    title = factory.Faker("sentence", nb_words=12)
    content = factory.Faker("sentence", nb_words=100)

    @factory.lazy_attribute
    def created_at(self) -> datetime:
        days = secrets.randbelow(61)
        dt = datetime.now() - timedelta(days=days)
        return timezone.make_aware(dt)
