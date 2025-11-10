from app.domain.interfaces.user_interface import UserRepository
from app.domain.interfaces.password_interface import PasswordValidator, PasswordHasher
from typing import Optional
from app.domain.entities.user import User


class AuthValidator:

    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
        password_validator: PasswordValidator
    ) -> None:
        self.user_repo = user_repository
        self.password_hasher = password_hasher
        self.password_validator = password_validator

    async def validate_registration(
        self, email: str, username: str, password: str
    ) -> None:
        if await self.user_repo.get_by_email(email):
            raise ValueError("User with this email already exists")

        if await self.user_repo.get_by_username(username):
            raise ValueError("User with this username already exists")

        self.password_validator.validate(password)

    def validate_verify(self, user_entity: Optional[User]) -> None:
        if not user_entity:
            raise ValueError("The user with this uuid was not found")
        if user_entity.email_confirmed:
            raise ValueError("Email уже подтвержден")

        self.chek_delete_or_block(user_entity)

    def validate_login(self, user_entity: Optional[User], password: str):
        if not user_entity or not self.password_hasher.verify(
            password, user_entity.password_hash
        ):
            raise ValueError("Неверный логин или пароль")

        if not user_entity.email_confirmed:
            raise ValueError("Подтвердите email для входа")

        self.chek_delete_or_block(user_entity)

    def chek_delete_or_block(self, user_entity: User) -> None:
        if not user_entity.is_active:
            raise ValueError("Аккаунт заблокирован")
        if user_entity.is_deleted:
            raise ValueError("Пользователь удален")
