from typing import Optional
from sqlalchemy.future import select
from uuid import UUID
from domain.interfaces.user_interface import UserRepository
from domain.entities.user import User
from infrastructure.persistence.sqlalchemy.models.user import UserORM
from infrastructure.persistence.sqlalchemy.repositories.base_repository import SQLAlchemyBaseRepository


class SQLAlchemyUserRepository(UserRepository, SQLAlchemyBaseRepository):

    async def get_by_email(self, email: str) -> Optional[User]:
        orm_user = await self.db_session.scalar(
            select(UserORM).where(UserORM.email == email)
        )
        if orm_user is not None:
            user_data = self.dict_for_entity(orm_user)
            return self.create_from_data(user_data)

    async def get_by_username(self, username: str) -> Optional[User]:
        orm_user = await self.db_session.scalar(
            select(UserORM).where(UserORM.username == username)
        )
        if orm_user is not None:
            user_data = self.dict_for_entity(orm_user)
            return self.create_from_data(user_data)

    async def get_by_id(self, id: UUID) -> Optional[User]:
        orm_user = await self.db_session.scalar(select(UserORM).where(UserORM.id == id))
        if orm_user is not None:
            user_data = self.dict_for_entity(orm_user)
            return self.create_from_data(user_data)

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
        user_data = self.dict_for_entity(new_user)
        return self.create_from_data(user_data)

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

        user_data = self.dict_for_entity(orm_user)
        return self.create_from_data(user_data)

    async def delete(self, id: UUID) -> bool:
        orm_user = await self.db_session.scalar(select(UserORM).where(UserORM.id == id))
        if orm_user is None:
            return False

        orm_user.is_deleted = True
        await self.db_session.commit()
        await self.db_session.refresh(orm_user)
        return True
