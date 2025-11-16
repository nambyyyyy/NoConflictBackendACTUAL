from typing import Optional
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from domain.interfaces.conflict_interface import ConflictRepository
from domain.entities.conflict import Conflict
from infrastructure.persistence.sqlalchemy.models.conflict import ConflictORM
from infrastructure.persistence.sqlalchemy.repositories.base_repository import (
    SQLAlchemyBaseRepository,
)
from uuid import UUID


class SQLAlchemyConflictRepository(ConflictRepository, SQLAlchemyBaseRepository):

    async def get_by_id(self, conflict_id: UUID) -> Optional[Conflict]:
        orm_conflict = await self.db_session.scalar(
            select(ConflictORM)
            .where(ConflictORM.id == conflict_id)
            .options(selectinload(ConflictORM.items), selectinload(ConflictORM.events))
        )
        if orm_conflict is not None:
            conflict_data = self.dict_for_entity(orm_conflict)
            return self.create_from_data(conflict_data)

    async def get_by_slug(self, slug: str) -> Optional[Conflict]:
        orm_conflict = await self.db_session.scalar(
            select(ConflictORM)
            .where(ConflictORM.slug == slug)
            .options(selectinload(ConflictORM.items), selectinload(ConflictORM.events))
        )
        if orm_conflict is not None:
            conflict_data = self.dict_for_entity(orm_conflict)
            return self.create_from_data(conflict_data)

    async def create(self, conflict: Conflict) -> Conflict:
        new_conflict = ConflictORM(
            title=conflict.title,
            creator_id=conflict.creator_id,
            id=conflict.id,
            slug=conflict.slug,
        )
        self.db_session.add(new_conflict)
        await self.db_session.commit()
        await self.db_session.refresh(new_conflict)

        orm_conflict = await self.db_session.scalar(
            select(ConflictORM)
            .where(ConflictORM.id == new_conflict.id)
            .options(
                selectinload(ConflictORM.items),
                selectinload(ConflictORM.events),
            )
        )

        conflict_data = self.dict_for_entity(orm_conflict)
        return self.create_from_data(conflict_data)

    async def update(
        self,
        conflict: Conflict,
        update_fields: Optional[list[str]] = None,
        return_none=False,
    ) -> Optional[Conflict]:
        orm_conflict = await self.db_session.scalar(
            select(ConflictORM).where(ConflictORM.id == conflict.id)
        )

        if orm_conflict is None:
            return None

        fields_to_update = (
            update_fields
            if update_fields is not None
            else [
                "creator_id",
                "creator_username",
                "partner_id",
                "partner_username",
                "title",
                "status",
                "slug",
                "progress",
                "created_at",
                "resolved_at",
                "truce_status",
                "truce_initiator_id",
                "truce_initiator_username",
                "items",
                "events",
            ]
        )

        for field in fields_to_update:
            if hasattr(conflict, field):
                setattr(orm_conflict, field, getattr(conflict, field))

        await self.db_session.commit()
        await self.db_session.refresh(orm_conflict)

        if return_none:
            return

        conflict_data = self.dict_for_entity(orm_conflict)
        return self.create_from_data(conflict_data)

    async def delete(self, slug: str):
        pass
