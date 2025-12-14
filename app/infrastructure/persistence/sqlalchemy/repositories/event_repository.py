from domain.interfaces.event_interface import EventRepository
from domain.entities.conflict_event import ConflictEvent
from infrastructure.persistence.sqlalchemy.models.conflict_event import (
    ConflictEventORM,
)
from infrastructure.persistence.sqlalchemy.repositories.base_repository import (
    SQLAlchemyBaseRepository,
)


class SQLAlchemyConflictEventRepository(EventRepository, SQLAlchemyBaseRepository):

    async def create(self, event: ConflictEvent) -> None:
        new_event = ConflictEventORM(
            id=event.id,
            conflict_id=event.conflict_id,
            item_id=event.item_id,
            initiator_id=event.initiator_id,
            event_type=event.event_type,
            old_value=event.old_value,
            new_value=event.new_value,
        )
        self.db_session.add(new_event)
        try:
            await self.db_session.flush()
        except Exception as e:
            print(e)