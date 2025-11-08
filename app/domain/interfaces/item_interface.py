from abc import ABC, abstractmethod
from domain.entities.conflict_item import ConflictItem
from typing import Optional
from uuid import UUID


class ItemRepository(ABC):

    @abstractmethod
    async def create(
        self,
        item: ConflictItem,
    ) -> Optional[ConflictItem]:
        """Создать item конфликта"""
        pass

    async def update(
        self,
        item: ConflictItem,
        update_fields: Optional[list[str]] = None,
    ) -> Optional[ConflictItem]:
        """Обновить item конфликта"""
        pass

    @abstractmethod
    async def get_by_id_and_conflict_id(
        self, item_id: UUID, conflict_id: UUID
    ) -> Optional[ConflictItem]:
        """Найти item по item_id и conflict_id"""
        pass
