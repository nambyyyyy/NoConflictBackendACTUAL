from abc import ABC
from dataclasses import dataclass
from uuid import UUID
from app.domain.entities.user import User

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
    
    @classmethod
    def create_dto(cls, user_entity: User) -> "UserDTO":
        return cls(
            id=user_entity.id,
            email=user_entity.email,
            username=user_entity.username,
            email_confirmed=user_entity.email_confirmed,
        )