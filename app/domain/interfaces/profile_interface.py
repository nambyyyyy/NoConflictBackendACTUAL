from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID
from domain.entities.profile import Profile


class ProfileRepository(ABC):
    
    @abstractmethod
    async def get_by_id(self, profile_id: UUID) -> Optional[Profile]:
        """Найти профиль по ID"""
        pass

    @abstractmethod
    async def get_by_user_id(self, user_id: UUID) -> Optional[Profile]:
        """Найти профиль по ID пользователя (основной метод!)"""
        pass
    
    @abstractmethod
    async def create(self, profile: Profile) -> Profile:
        """Создать профиль"""
        pass
    

    @abstractmethod
    async def update(self, profile: Profile) -> Optional[Profile]:
        """Обновить профиль"""
        pass

