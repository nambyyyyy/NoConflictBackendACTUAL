from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from app.domain.interfaces.conflict_interface import ConflictRepository
from app.domain.entities.conflict import Conflict
from app.domain.entities.conflict_item import ConflictItem
from app.domain.entities.conflict_event import ConflictEvent
from app.infrastructure.persistence.sqlalchemy.models.conflict import ConflictORM


class SQLAlchemyConflictRepository(ConflictRepository):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_by_id(self, conflict_id: UUID) -> Optional[Conflict]:
        orm_conflict = await self.db_session.scalar(
            select(ConflictORM).where(ConflictORM.id == conflict_id)
        )
        if orm_conflict is not None:
            return self._to_entity_conflict(orm_conflict)

    async def get_by_slug(self, slug: str) -> Optional[Conflict]:
        orm_conflict = await self.db_session.scalar(
            select(ConflictORM).where(ConflictORM.slug == slug)
        )
        if orm_conflict is not None:
            return self._to_entity_conflict(orm_conflict)

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
        return self._to_entity_conflict(new_conflict)

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
        return self._to_entity_conflict(orm_conflict)
    
    async def delete(self, slug: str):
        pass
    
    def _to_entity_items(self, orm_conflict: ConflictORM) -> list[ConflictItem]:
        items_data = [
            ConflictItem(
                id=item.id,
                conflict_id=orm_conflict.id,
                title=item.title,
                creator_choice_value=item.creator_choice_value,
                partner_choice_value=item.partner_choice_value,
                agreed_choice_value=item.agreed_choice_value,
                is_agreed=item.is_agreed,
            )
            for item in orm_conflict.items.all()
        ]
        return items_data

    def _to_entity_events(self, orm_conflict: ConflictORM) -> list[ConflictEvent]:
        events_data = [
            ConflictEvent(
                id=event.id,
                conflict_id=orm_conflict.id,
                created_at=event.created_at,
                initiator_id=event.initiator.id if event.initiator else None,
                initiator_username=(
                    event.initiator.username if event.initiator else None
                ),
                event_type=event.event_type,
                item_id=event.item.id if event.item else None,
                item_title=event.item.title if event.item else None,
                old_value=event.old_value,
                new_value=event.new_value,
            )
            for event in orm_conflict.events.all()
        ]
        return events_data

    def _to_entity_conflict(self, orm_conflict: ConflictORM) -> Conflict:
        """Приватный метод конвертации"""
        return Conflict(
            id=orm_conflict.id,
            creator_id=orm_conflict.creator.id,
            creator_username=(
                orm_conflict.creator.username if orm_conflict.creator.username else None
            ),
            partner_id=orm_conflict.partner.id if orm_conflict.partner else None,
            partner_username=(
                orm_conflict.partner.username if orm_conflict.partner else None
            ),
            title=orm_conflict.title,
            status=orm_conflict.status,
            slug=orm_conflict.slug,
            progress=orm_conflict.progress,
            created_at=orm_conflict.created_at,
            resolved_at=orm_conflict.resolved_at,
            deleted_by_creator=orm_conflict.deleted_by_creator,
            deleted_by_partner=orm_conflict.deleted_by_partner,
            truce_status=orm_conflict.truce_status,
            truce_initiator_id=(
                orm_conflict.truce_initiator.id
                if orm_conflict.truce_initiator
                else None
            ),
            truce_initiator_username=(
                orm_conflict.truce_initiator.username
                if orm_conflict.truce_initiator
                else None
            ),
            items=self._to_entity_items(orm_conflict),
            events=self._to_entity_events(orm_conflict),
        )
