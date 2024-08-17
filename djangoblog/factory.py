import random
from datetime import datetime, timedelta

import factory

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
    def created_at(self):
        return datetime.now() - timedelta(days=random.randint(0, 60))
