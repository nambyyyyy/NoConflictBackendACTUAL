from typing import Protocol, Type, TypeVar, Any

T = TypeVar("T", bound="EntityProtocol", covariant=True)

class EntityProtocol(Protocol[T]):
    @classmethod
    def create_entity(cls, **kwargs: Any) -> T:
        ...