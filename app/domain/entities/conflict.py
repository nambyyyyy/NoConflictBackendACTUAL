from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID
from domain.entities.conflict_item import ConflictItem
from domain.entities.conflict_event import ConflictEvent


class ConflictError(Exception):
    """Любая доменная ошибка по конфликтам."""


@dataclass
class Conflict:
    title: str
    id: UUID
    creator_id: UUID
    slug: str
    created_at: datetime
    creator_username: Optional[str] = None
    partner_id: Optional[UUID] = None
    partner_username: Optional[str] = None

    status: str = "pending"  # pending / in_progress / resolved / cancelled / abandoned

    progress: float = 0.0
    resolved_at: Optional[datetime] = None

    deleted_by_creator: bool = False
    deleted_by_partner: bool = False
    is_deleted: bool = False
    deleted_at: Optional[datetime] = None

    truce_status: str = "none"  # none / pending / accepted
    truce_initiator_id: Optional[UUID] = None
    truce_initiator_username: Optional[str] = None

    items: list["ConflictItem"] = field(default_factory=list)
    events: list["ConflictEvent"] = field(default_factory=list)

    @classmethod
    def create_entity(
        cls,
        title: str,
        id: UUID,
        creator_id: UUID,
        slug: str,
        created_at: datetime,
        **kwargs
    ) -> "Conflict":
        items = [ConflictItem.create_entity(**data) for data in kwargs.pop("items", [])]
        events = [ConflictEvent.create_entity(**data) for data in kwargs.pop("events", [])]
        
        return cls(
            title=title,
            id=id,
            creator_id=creator_id,
            slug=slug,
            created_at=created_at,
            items=items,
            events=events,
            **kwargs
        )
