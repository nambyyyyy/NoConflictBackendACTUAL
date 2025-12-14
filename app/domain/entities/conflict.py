from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID
from domain.entities.conflict_item import ConflictItem
from domain.entities.conflict_event import ConflictEvent
import enum


class ConflictError(Exception):
    """Любая доменная ошибка по конфликтам."""
    
    
class ConflictStatusEnum(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CANCELLED = "cancelled"
    ABANDONED = "abandoned"   

class TruceStatusEnum(str, enum.Enum):
    NONE = "none"
    PENDING = "pending"
    ACCEPTED = "accepted"


@dataclass
class Conflict:
    id: UUID
    title: str
    creator_id: UUID
    slug: str
    
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    creator_username: Optional[str] = None
    partner_id: Optional[UUID] = None
    partner_username: Optional[str] = None

    status: ConflictStatusEnum = ConflictStatusEnum.PENDING  # pending / in_progress / resolved / cancelled / abandoned

    progress: float = 0.0
    resolved_at: Optional[datetime] = None

    deleted_by_creator: bool = False
    deleted_by_partner: bool = False
    is_deleted: bool = False
    deleted_at: Optional[datetime] = None

    truce_status: TruceStatusEnum = TruceStatusEnum.NONE  # none / pending / accepted
    truce_initiator_id: Optional[UUID] = None
    truce_initiator_username: Optional[str] = None

    items: list["ConflictItem"] = field(default_factory=list)
    events: list["ConflictEvent"] = field(default_factory=list)

    
    @classmethod
    def create_entity(
        cls,
        id: UUID,
        title: str,
        creator_id: UUID,
        slug: str,
        **kwargs
    ) -> "Conflict":
        items = [ConflictItem.create_entity(**data) for data in kwargs.pop("items", [])]
        events = [ConflictEvent.create_entity(**data) for data in kwargs.pop("events", [])]
        
        return cls(
            id=id,
            title=title,
            creator_id=creator_id,
            slug=slug,
            items=items,
            events=events,
            **kwargs
        )
