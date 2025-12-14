from dataclasses import dataclass
from typing import Protocol, Type, TypeVar, Any, Optional
from uuid import UUID
from datetime import datetime


@dataclass
class ConflictItem:
    id: UUID
    conflict_id: UUID
    title: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    creator_choice_value: Optional[str] = None
    partner_choice_value: Optional[str] = None
    agreed_choice_value: Optional[str] = None
    is_agreed: bool = False

    @classmethod
    def create_entity(
        cls, id: UUID, conflict_id: UUID, title: str, **kwargs
    ) -> "ConflictItem":

        return cls(id=id, conflict_id=conflict_id, title=title, **kwargs)
