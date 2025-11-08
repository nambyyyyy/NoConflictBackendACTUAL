from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from app.domain.interfaces.profile_interface import ProfileRepository
from app.domain.entities.profile import Profile
from app.infrastructure.persistence.sqlalchemy.models.profile import ProfileORM


class SQLAlchemyProfileRepository(ProfileRepository):

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_by_id(self, profile_id: UUID) -> Optional[Profile]:
        """Найти профиль по ID"""
        orm_profile = await self.db_session.scalar(
            select(ProfileORM).where(ProfileORM.id == profile_id)
        )
        if orm_profile is not None:
            return self._to_entity(orm_profile)

    async def get_by_user_id(self, user_id: UUID) -> Optional[Profile]:
        """Найти профиль по ID пользователя (основной метод!)"""
        orm_profile = await self.db_session.scalar(
            select(ProfileORM).where(ProfileORM.user_id == user_id)
        )
        if orm_profile is not None:
            return self._to_entity(orm_profile)

    async def create(self, profile: Profile) -> Profile:
        """Создание профиля"""
        new_profile = ProfileORM(
            id=profile.id,
            user_id=profile.user_id,
        )
        self.db_session.add(new_profile)
        await self.db_session.commit()
        await self.db_session.refresh(new_profile)
        return self._to_entity(new_profile)

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
        return self._to_entity(orm_profile)

    def _to_entity(self, orm_profile: ProfileORM) -> Profile:
        """Приватный метод конвертации"""
        return Profile(
            id=orm_profile.id,
            user_id=orm_profile.user.id,
            first_name=orm_profile.first_name,
            last_name=orm_profile.last_name,
            gender=orm_profile.gender,
            avatar_filename=orm_profile.avatar_filename,
            location=orm_profile.location,
            bio=orm_profile.bio,
            created_at=orm_profile.created_at,
            updated_at=orm_profile.updated_at,
        )
