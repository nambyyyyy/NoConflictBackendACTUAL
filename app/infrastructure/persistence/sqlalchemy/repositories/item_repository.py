from typing import Optional
from sqlalchemy.future import select
from uuid import UUID
from domain.interfaces.item_interface import ItemRepository
from domain.entities.conflict_item import ConflictItem
from infrastructure.persistence.sqlalchemy.models.conflict_item import (
    ConflictItemORM,
)
from infrastructure.persistence.sqlalchemy.repositories.base_repository import (
    SQLAlchemyBaseRepository,
)


class SQLAlchemyConflictItemRepository(ItemRepository, SQLAlchemyBaseRepository):

    async def get_by_id_and_conflict_id(
        self, item_id: UUID, conflict_id: UUID
    ) -> Optional[ConflictItem]:
        orm_item = await self.db_session.scalar(
            select(ConflictItemORM).where(
                ConflictItemORM.id == item_id,
                ConflictItemORM.conflict_id == conflict_id,
            )
        )
        if orm_item is not None:
            item_data = self.fast_dict_for_entity(orm_item)
            return self.create_from_data(item_data)

    async def create(self, item: ConflictItem) -> Optional[ConflictItem]:
        new_item = ConflictItemORM(
            conflict_id=item.conflict_id,
            title=item.title,
            creator_choice_value=item.creator_choice_value,
        )
        self.db_session.add(new_item)
        await self.db_session.commit()
        await self.db_session.refresh(new_item)
        
        item_data = self.fast_dict_for_entity(new_item)
        return self.create_from_data(item_data)

    async def update(
        self, item: ConflictItem, update_fields: Optional[list[str]] = None
    ) -> Optional[ConflictItem]:
        orm_item = await self.db_session.scalar(
            select(ConflictItemORM).where(ConflictItemORM.id == item.id)
        )

        if orm_item is None:
            return None

        fields_to_update = (
            update_fields
            if update_fields is not None
            else [
                "title",
                "creator_choice_value",
                "partner_choice_value",
                "agreed_choice_value",
                "is_agreed",
            ]
        )

        for field in fields_to_update:
            if hasattr(item, field):
                setattr(orm_item, field, getattr(item, field))

        await self.db_session.commit()
        await self.db_session.refresh(orm_item)
        
        item_data = self.fast_dict_for_entity(orm_item)
        return self.create_from_data(item_data)
    
