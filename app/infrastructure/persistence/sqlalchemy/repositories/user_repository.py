from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from app.domain.interfaces.user_interface import UserRepository
from app.domain.entities.user import User
from app.infrastructure.persistence.sqlalchemy.models.user import UserORM


class SQLAlchemyUserRepository(UserRepository):

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_by_email(self, email: str) -> Optional[User]:
        orm_user = await self.db_session.scalar(
            select(UserORM).where(UserORM.email == email)
        )
        if orm_user is not None:
            return self._to_entity(orm_user)

    async def get_by_username(self, username: str) -> Optional[User]:
        orm_user = await self.db_session.scalar(
            select(UserORM).where(UserORM.username == username)
        )
        if orm_user is not None:
            return self._to_entity(orm_user)

    async def get_by_id(self, id: UUID) -> Optional[User]:
        orm_user = await self.db_session.scalar(select(UserORM).where(UserORM.id == id))
        if orm_user is not None:
            return self._to_entity(orm_user)

    async def create(self, user: User) -> Optional[User]:
        new_user = UserORM(
            id=user.id,
            email=user.email,
            username=user.username,
            password=user.password_hash,
            email_confirmed=user.email_confirmed,
            is_active=user.is_active,
        )
        self.db_session.add(new_user)
        await self.db_session.commit()
        await self.db_session.refresh(new_user)
        return self._to_entity(new_user)

    async def update(
        self, user: User, update_fields: Optional[list[str]] = None
    ) -> Optional[User]:
        orm_user = await self.db_session.scalar(
            select(UserORM).where(UserORM.id == user.id)
        )

        if orm_user is None:
            return None

        fields_to_update = (
            update_fields
            if update_fields is not None
            else ["email", "username", "password", "email_confirmed", "is_active"]
        )

        for field in fields_to_update:
            if hasattr(user, field):
                setattr(orm_user, field, getattr(user, field))

        await self.db_session.commit()
        await self.db_session.refresh(orm_user)

        return self._to_entity(orm_user)

    async def delete(self, id: UUID) -> bool:
        orm_user = await self.db_session.scalar(select(UserORM).where(UserORM.id == id))
        if orm_user is None:
            return False

        orm_user.is_deleted = True
        await self.db_session.commit()
        await self.db_session.refresh(orm_user)
        return True

    def _to_entity(self, orm_user: UserORM) -> User:
        """Приватный метод конвертации"""
        return User(
            id=orm_user.id,
            email=orm_user.email,
            username=orm_user.username,
            password_hash=orm_user.password,
            email_confirmed=orm_user.email_confirmed,
            is_active=orm_user.is_active,
            created_at=orm_user.created_at,
            updated_at=orm_user.updated_at,
        )
