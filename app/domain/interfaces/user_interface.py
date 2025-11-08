from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID
from domain.entities.user import User


class UserRepository(ABC):

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        """Найти пользователя по email (для проверки существования)"""
        pass

    @abstractmethod
    async def get_by_username(self, username: str) -> Optional[User]:
        """Найти пользователя по username (понадобится для подтверждения username)"""
        pass

    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        """Найти пользователя по ID (понадобится для подтверждения email)"""
        pass

    # @abstractmethod
    # async def get_by_id_model(self, user_id: UUID) -> Optional[User]:
    #     """Найти пользователя по ID и вернуть саму модель
    #     (понадобится для созданий связей в БД)"""
    #     pass

    # @abstractmethod
    # async def get_many_id(self, user_ids: list[UUID]) -> Optional[list[User]]:
    #     """Найти пользователя по ID (понадобится для подтверждения email)"""
    #     pass

    @abstractmethod
    async def create(self, user: User) -> User:
        """Создать пользователя)"""
        pass

    @abstractmethod
    async def update(
        self, user: User, update_fields: Optional[list[str]] = None
    ) -> User:
        """Обновить пользователя (для подтверждения email, смены пароля)"""
        pass

    @abstractmethod
    async def delete(self, user_id: UUID) -> None:
        """Удалить пользователя"""
        pass
