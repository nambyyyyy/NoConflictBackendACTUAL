from abc import ABC, abstractmethod
from domain.entities.conflict import Conflict
from uuid import UUID
from typing import TypeVar, Optional

T = TypeVar("T")


class ConflictRepository(ABC):

    @abstractmethod
    async def get_by_id(self, conflict_id: UUID) -> Optional[Conflict]:
        """Вернуть Conflict по conflict_id"""
        pass

    @abstractmethod
    async def get_by_slug(self, slug: str) -> Optional[Conflict]:
        """Вернуть Conflict по slug"""
        pass

    @abstractmethod
    async def create(self, conflict: Conflict) -> Conflict:
        """Создать конфликт"""
        pass

    @abstractmethod
    async def update(
        self,
        conflict: Conflict,
        update_fields: Optional[list[str]] = None,
        return_none=False,
    ) -> Conflict:
        """Обновить конфликт"""
        pass

    @abstractmethod
    async def delete(self, slug: str) -> bool:
        """Удлить конфликт по slug"""
        pass


