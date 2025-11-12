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
    email_confirmed: bool = False
    is_active: bool = True
    is_deleted: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    @classmethod
    def create_entity(
        cls,
        email: str,
        username: str,
        password_hash: str,
    ) -> "User":
        return cls(
            id=uuid4(),
            email=email,
            username=username,
            password_hash=password_hash,
            created_at=datetime.now(),
        )
    
    