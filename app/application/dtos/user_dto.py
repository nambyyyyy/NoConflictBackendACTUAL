from abc import ABC
from dataclasses import dataclass
from uuid import UUID

@dataclass
class UserDTO(ABC):
    """DTO для передачи данных о пользователе"""
    id: UUID
    email: str
    username: str
    email_confirmed: bool
    
    def to_dict(self):
        return {
            "id": str(self.id),
            "email": self.email,
            "username": self.username,
            "email_confirmed": self.email_confirmed
        }