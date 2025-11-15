from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

@dataclass
class User:
    id: UUID
    email: str
    username: str
    password_hash: str
    created_at: datetime
    email_confirmed: bool = False
    is_active: bool = True
    is_deleted: bool = False
    updated_at: Optional[datetime] = None
    
    @classmethod
    def create_entity(
        cls,
        id: UUID,
        email: str,
        username: str,
        password_hash: str,
        created_at: datetime,
        **kwargs
    ) -> "User":
            
        return cls(
            id=id,
            email=email,
            username=username,
            password_hash=password_hash,
            created_at=created_at,
            **kwargs
        )
    
    