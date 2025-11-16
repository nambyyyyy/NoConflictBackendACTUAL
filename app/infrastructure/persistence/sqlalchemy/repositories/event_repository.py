from domain.interfaces.event_interface import EventRepository
from domain.entities.conflict_event import ConflictEvent
from infrastructure.persistence.sqlalchemy.models.conflict_event import (
    ConflictEventORM,
)
from infrastructure.persistence.sqlalchemy.repositories.base_repository import (
    SQLAlchemyBaseRepository,
)


class SQLAlchemyConflictEventRepository(EventRepository, SQLAlchemyBaseRepository):

    async def create(self, event: ConflictEvent) -> ConflictEvent:
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
        return self.create_from_data(event_data)
