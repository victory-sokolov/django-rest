from typing import Protocol, TypeVar

T = TypeVar("T", covariant=True)


class IRepository(Protocol[T]):
    def get(self) -> T: ...

    def get_all(self) -> T: ...

    def create(self) -> T: ...
