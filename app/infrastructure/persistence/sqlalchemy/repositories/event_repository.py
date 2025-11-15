from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.interfaces.event_interface import EventRepository
from app.domain.entities.conflict_event import ConflictEvent
from app.infrastructure.persistence.sqlalchemy.models.conflict_event import (
    ConflictEventORM,
)
from app.infrastructure.persistence.sqlalchemy.repositories.base_repository import (
    UtilRepository,
)


class SQLAlchemyConflictEventRepository(EventRepository, UtilRepository):
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

        event_data = self.dict_for_entity(new_event)
        return ConflictEvent.create_entity(**event_data)
