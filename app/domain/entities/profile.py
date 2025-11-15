from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID


@dataclass
class Profile:
    id: UUID
    user_id: UUID
    avatar_filename: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    gender: Optional[str] = None
    location: Optional[str] = None
    bio: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def create_entity(cls, id: UUID, user_id: UUID, **kwargs) -> "Profile":
        return cls(id=id, user_id=user_id, **kwargs)
