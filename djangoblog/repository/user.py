from djangoblog.models import UserProfile
from djangoblog.repository.base import IRepository


class UserRepository(IRepository):
    def __init__(self) -> None:
        self.user = UserProfile.objects

    def get(self, user_id: str):
        return self.user.get(user_id)

    def create(self) -> None: ...

    def get_all(self) -> None: ...
