from uuid import UUID
from typing import Optional
from datetime import datetime
from abc import ABC
from dataclasses import dataclass


@dataclass
class ProfileDTO(ABC):
    """DTO для отдачи данных профиля на клиент"""
    id: UUID
    user_id: UUID
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    full_name: Optional[str] = None
    gender: Optional[str] = None
    location: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None