from uuid import UUID
from typing import Optional, List
from datetime import datetime
from dataclasses import dataclass
from app.application.dtos.base_dto import BaseDTO


@dataclass
class ConflictItemDTO(BaseDTO):
    id: UUID
    title: str
    creator_choice_value: Optional[str]
    partner_choice_value: Optional[str]
    agreed_choice_value: Optional[str]
    is_agreed: bool
    

@dataclass
class ConflictEventDTO(BaseDTO):
    id: UUID
    event_type: str
    created_at: datetime
    initiator_id: Optional[UUID]
    initiator_username: Optional[str]
    item_id: Optional[UUID]
    item_title: Optional[str]
    old_value: Optional[str]
    new_value: Optional[str]
    

@dataclass
class ConflictDetailDTO(BaseDTO):
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
    

@dataclass
class ConflictShortDTO(BaseDTO):
    id: UUID
    creator_id: UUID
    creator_username: Optional[str]
    partner_id: Optional[UUID]
    partner_username: Optional[str]
    title: Optional[str]
    status: str
    progress: float
    resolved_at: Optional[datetime]
    
