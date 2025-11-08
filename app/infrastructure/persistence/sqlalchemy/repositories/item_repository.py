from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from app.domain.interfaces.item_interface import ItemRepository
from app.domain.entities.conflict_item import ConflictItem
from app.infrastructure.persistence.sqlalchemy.models.conflict_item import (
    ConflictItemORM,
)


class SQLAlchemyConflictItemRepository(ItemRepository):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

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
            return self._to_entity(orm_item)

    async def create(self, item: ConflictItem) -> Optional[ConflictItem]:
        new_item = ConflictItemORM(
            conflict_id=item.conflict_id,
            title=item.title,
            creator_choice_value=item.creator_choice_value,
        )
        self.db_session.add(new_item)
        await self.db_session.commit()
        await self.db_session.refresh(new_item)
        return self._to_entity(new_item)

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
        return self._to_entity(orm_item)
    
    def _to_entity(self, orm_item: ConflictItemORM) -> ConflictItem:
        return ConflictItem(
            id=orm_item.id,
            conflict_id=orm_item.conflict_id,
            title=orm_item.title,
            creator_choice_value=orm_item.creator_choice_value,
            partner_choice_value=orm_item.partner_choice_value,
            agreed_choice_value=orm_item.agreed_choice_value,
            is_agreed=orm_item.is_agreed,
        )
