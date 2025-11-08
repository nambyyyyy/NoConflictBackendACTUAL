from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional, List, Dict


class ConflictItem(BaseModel):
    title: str = Field(..., max_length=255)
    creator_choice_value: Optional[str] = None
    partner_choice_value: Optional[str] = None
    agreed_choice_value: Optional[str] = None


class CreateConflict(BaseModel):
    partner_id: Optional[UUID] = None
    title: str = Field(..., max_length=255)
    items: List[ConflictItem] = Field(..., min_items=1) # type: ignore


class ConflictDetailResponse(BaseModel):
    id: UUID
    creator_id: UUID
    creator_username: Optional[str] = None
    partner_id: Optional[UUID] = None
    partner_username: Optional[str] = None
    title: str
    status: str
    slug: str
    progress: float
    created_at: datetime
    resolved_at: Optional[datetime] = None
    truce_status: str
    truce_initiator_id: Optional[UUID] = None
    truce_initiator_username: Optional[str] = None
    items: List[Dict] = Field(default_factory=list)
    events: List[Dict] = Field(default_factory=list)
    