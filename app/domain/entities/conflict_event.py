from dataclasses import dataclass
from typing import Optional
from uuid import UUID
from datetime import datetime



@dataclass
class ConflictEvent:
    id: UUID
    conflict_id: UUID
    event_type: str
    created_at: datetime
    initiator_id: Optional[UUID] = None
    initiator_username: Optional[str] = None
    item_id: Optional[UUID] = None
    item_title: Optional[str] = None
    old_value: Optional[str] = None
    new_value: Optional[str] = None

    @classmethod
    def create_entity(
        cls,
        id: UUID,
        conflict_id: UUID,
        event_type: str,
        created_at: datetime,
        **kwargs
    ) -> "ConflictEvent":
        initiator = kwargs.pop("initiator", None)
        item = kwargs.pop("item", None)

        return cls(
            id=id,
            conflict_id=conflict_id,
            event_type=event_type,
            created_at=created_at,
            initiator_id=getattr(initiator, "id", None),
            initiator_username=getattr(initiator, "username", None),
            item_id=getattr(item, "id", None),
            item_title=getattr(item, "title", None),
            **kwargs,
        )