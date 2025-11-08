from uuid import UUID
from typing import Optional, List
from datetime import datetime
from abc import ABC
from dataclasses import dataclass


@dataclass
class ConflictItemDTO(ABC):
    id: UUID
    title: str
    creator_choice_value: Optional[str]
    partner_choice_value: Optional[str]
    agreed_choice_value: Optional[str]
    is_agreed: bool
    
    def to_dict(self):
        return {
            "id": str(self.id),
            "title": self.title,
            "creator_choice_value": self.creator_choice_value,
            "partner_choice_value": self.partner_choice_value,
            "agreed_choice_value": self.agreed_choice_value,
            "is_agreed": self.is_agreed,
        }

@dataclass
class ConflictEventDTO(ABC):
    id: UUID
    event_type: str
    created_at: datetime
    initiator_id: Optional[UUID]
    initiator_username: Optional[str]
    item_id: Optional[UUID]
    item_title: Optional[str]
    old_value: Optional[str]
    new_value: Optional[str]
    
    def to_dict(self):
        return {
            "id": str(self.id),
            "event_type": self.event_type,
            "created_at": self.created_at.isoformat(),
            "initiator_id": str(self.initiator_id) if str(self.initiator_id) else None,
            "initiator_username": self.initiator_username,
            "item_id": str(self.item_id) if self.item_id else None,
            "item_title": self.item_title,
            "old_value": self.old_value,
            "new_value": self.new_value,
        }

@dataclass
class ConflictDetailDTO(ABC):
    id: UUID
    creator_id: UUID
    creator_username: Optional[str]
    partner_id: Optional[UUID]
    partner_username: Optional[str]
    title: Optional[str]
    status: str
    slug: str
    progress: float
    created_at: datetime
    resolved_at: Optional[datetime]
    truce_status: str
    truce_initiator_id: Optional[UUID]
    truce_initiator_username: Optional[str]
    items: List[ConflictItemDTO]
    events: List[ConflictEventDTO]
    
    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "creator_id": str(self.creator_id),
            "creator_username": self.creator_username,
            "partner_id": str(self.partner_id),
            "partner_username": self.partner_username,
            "title": self.title,
            "status": self.status,
            "slug": self.slug,
            "progress": self.progress,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "resolved_at": self.resolved_at.isoformat() if self.resolved_at else None,
            "truce_status": self.truce_status,
            "truce_initiator_id": (
                str(self.truce_initiator_id) if self.truce_initiator_id else None
            ),
            "truce_initiator_username": self.truce_initiator_username,
            "items": [item.to_dict() for item in self.items],
            "events": [event.to_dict() for event in self.events],
        }

@dataclass
class ConflictShortDTO(ABC):
    id: UUID
    creator_id: UUID
    creator_username: Optional[str]
    partner_id: Optional[UUID]
    partner_username: Optional[str]
    title: Optional[str]
    status: str
    progress: float
    resolved_at: Optional[datetime]
    
    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "creator_id": str(self.creator_id),
            "creator_username": self.creator_username,
            "partner_id": str(self.partner_id) if self.partner_id else None,
            "partner_username": self.partner_username,
            "title": self.title,
            "status": self.status,
            "progress": self.progress,
            "resolved_at": self.resolved_at.isoformat() if self.resolved_at else None,
        }