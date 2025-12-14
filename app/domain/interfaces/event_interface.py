from abc import ABC, abstractmethod
from domain.entities.conflict_event import ConflictEvent
from typing import Optional



    
    
class EventRepository(ABC):

    @abstractmethod
    async def create(
        self,
        event: ConflictEvent
    ) -> None:
        """Создать event конфликта"""
        pass