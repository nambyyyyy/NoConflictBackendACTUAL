from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import uuid4, UUID
from domain.entities.conflict_item import ConflictItem
from domain.entities.conflict_event import ConflictEvent

class ConflictError(Exception):
    """Любая доменная ошибка по конфликтам."""


@dataclass
class Conflict:
    title: str
    creator_id: UUID
    creator_username: Optional[str] = None
    partner_id: Optional[UUID] = None 
    partner_username: Optional[str] = None
    
    id: UUID = field(default_factory=uuid4)
    status: str = "pending"  # pending / in_progress / resolved / cancelled / abandoned
    slug: str = field(default_factory=lambda: str(uuid4()))

    progress: float = 0.0
    created_at: datetime = field(default_factory=datetime.utcnow)
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
    
