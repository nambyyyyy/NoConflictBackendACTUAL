from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from app.domain.interfaces.profile_interface import ProfileRepository
from app.domain.entities.profile import Profile
from app.infrastructure.persistence.sqlalchemy.models.profile import ProfileORM
from app.infrastructure.persistence.sqlalchemy.repositories.base_repository import UtilRepository

class SQLAlchemyProfileRepository(ProfileRepository, UtilRepository):

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_by_id(self, profile_id: UUID) -> Optional[Profile]:
        """Найти профиль по ID"""
        orm_profile = await self.db_session.scalar(
            select(ProfileORM).where(ProfileORM.id == profile_id)
        )
        if orm_profile is not None:
            profile_data = self.dict_for_entity(orm_profile)
            return Profile.create_entity(**profile_data)

    async def get_by_user_id(self, user_id: UUID) -> Optional[Profile]:
        """Найти профиль по ID пользователя (основной метод!)"""
        orm_profile = await self.db_session.scalar(
            select(ProfileORM).where(ProfileORM.user_id == user_id)
        )
        if orm_profile is not None:
            profile_data = self.dict_for_entity(orm_profile)
            return Profile.create_entity(**profile_data)

    async def create(self, profile: Profile) -> Profile:
        """Создание профиля"""
        new_profile = ProfileORM(
            id=profile.id,
            user_id=profile.user_id,
        )
        self.db_session.add(new_profile)
        await self.db_session.commit()
        await self.db_session.refresh(new_profile)
        
        profile_data = self.dict_for_entity(new_profile)
        return Profile.create_entity(**profile_data)

    async def update(
        self, profile: Profile, update_fields: Optional[list[str]] = None
    ) -> Optional[Profile]:
        """Обновление существующего профиля"""
        orm_profile = await self.db_session.scalar(
            select(ProfileORM).where(ProfileORM.id == profile.id)
        )
        if orm_profile is None:
            return None

        fields_to_update = (
            update_fields
            if update_fields is not None
            else [
                "first_name",
                "last_name",
                "gender",
                "avatar_filename",
                "location",
                "bio",
            ]
        )

        for field in fields_to_update:
            if hasattr(profile, field):
                setattr(orm_profile, field, getattr(profile, field))

        await self.db_session.commit()
        await self.db_session.refresh(orm_profile)
        
        profile_data = self.dict_for_entity(orm_profile)
        return Profile.create_entity(**profile_data)

