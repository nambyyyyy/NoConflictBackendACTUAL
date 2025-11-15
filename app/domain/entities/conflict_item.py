from dataclasses import dataclass
from typing import Optional
from uuid import UUID


@dataclass
class ConflictItem:
    id: UUID
    conflict_id: UUID
    title: str
    creator_choice_value: Optional[str] = None
    partner_choice_value: Optional[str] = None
    agreed_choice_value: Optional[str] = None
    is_agreed: bool = False

    @classmethod
    def create_entity(
        cls, id: UUID, conflict_id: UUID, title: str, **kwargs
    ) -> "ConflictItem":

        return cls(id=id, conflict_id=conflict_id, title=title, **kwargs)
