from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from app.domain.interfaces.event_interface import EventRepository
from app.domain.entities.conflict_event import ConflictEvent
from app.infrastructure.persistence.sqlalchemy.models.conflict_event import (
    ConflictEventORM
)


class SQLAlchemyConflictEventRepository(EventRepository):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        
    async def create(self, event: ConflictEvent) -> Optional[ConflictEvent]:
        new_event = ConflictEventORM(
            conflict_id=event.conflict_id,
            item_id=event.item_id,
            initiator_id=event.initiator_id,
            event_type=event.event_type,
            old_value=event.old_value,
            new_value=event.new_value,
        )
        self.db_session.add(new_event)
        await self.db_session.commit()
        await self.db_session.refresh(new_event)
        return self._to_entity(new_event)
    
    def _to_entity(self, orm_event: ConflictEventORM) -> ConflictEvent:
        return ConflictEvent(
            id=orm_event.id,
            conflict_id=orm_event.conflict_id,
            created_at=orm_event.created_at,
            initiator_id=(
                orm_event.initiator.id if orm_event.initiator.id else None
            ),
            initiator_username=(
                orm_event.initiator.username
                if orm_event.initiator.username
                else None
            ),
            event_type=orm_event.event_type,
            item_id=orm_event.item_id if orm_event.item_id else None,
            old_value=orm_event.old_value if orm_event.old_value else None,
            new_value=orm_event.new_value if orm_event.new_value else None,
        )