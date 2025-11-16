from abc import ABC, abstractmethod
from domain.entities.user import User

class EmailTokenRepository(ABC):
    """Интерфейс для токенов подтверждения email."""

    @abstractmethod
    def generate_token(self, user_id: str) -> str:
        pass

    @abstractmethod
    def verify_token(self, token: str, max_age: int = 3600) -> bool:
        pass


class JWTRepository(ABC):
    @abstractmethod
    def create_access_token(self, user: User) -> str:
        pass
    
    @abstractmethod
    def create_refresh_token(self, user: User) -> str:
        pass