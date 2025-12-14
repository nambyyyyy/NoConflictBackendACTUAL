from dataclasses import dataclass
from typing import Optional
from uuid import UUID
from datetime import datetime
import enum


class EventType(str, enum.Enum):
    TRUCE_OFFER = "TRUCE_OFFER"
    TRUCE_ACCEPTED = "TRUCE_ACCEPTED"
    TRUCE_DECLINED = "TRUCE_DECLINED"
    CONFLICT_DELETE = "CONFLICT_DELETE"
    CONFLICT_CANCEL = "CONFLICT_CANCEL"
    CONFLICT_RESOLVED = "CONFLICT_RESOLVED"
    ITEM_AGREED = "ITEM_AGREED"
    ITEM_ADD = "ITEM_ADD"
    ITEM_UPDATE = "ITEM_UPDATE"
    CONFLICT_JOIN_SUCCESS = "CONFLICT_JOIN_SUCCESS"
    CONFLICT_CREATE = "CONFLICT_CREATE"
    
    
@dataclass
class ConflictEvent:
    id: UUID
    conflict_id: UUID
    event_type: EventType
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
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
        event_type: EventType,
        **kwargs
    ) -> "ConflictEvent":

        return cls(
            id=id,
            conflict_id=conflict_id,
            event_type=event_type,
            **kwargs,
        )