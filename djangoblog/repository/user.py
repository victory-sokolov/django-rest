from djangoblog.api.v1.posts.types import UserId
from djangoblog.models import UserProfile
from djangoblog.repository.base import IRepository


class UserRepository(IRepository):
    def __init__(self) -> None:
        self.user = UserProfile.objects

    def get(self, user_id: UserId) -> UserProfile:
        return self.user.get(user_id)

    def create(self) -> None: ...

    def get_all(self) -> None: ...
