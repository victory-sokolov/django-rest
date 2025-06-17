from typing import Protocol, TypeVar, TypeVarTuple, Unpack

T = TypeVar("T", covariant=True)
ARGS = TypeVarTuple("ARGS")


class IRepository(Protocol[T, Unpack[ARGS]]):
    def get(self, *args: Unpack[ARGS]) -> T: ...
    def get_all(self, *args: Unpack[ARGS]) -> T: ...
    def create(self, *args: Unpack[ARGS]) -> T: ...
