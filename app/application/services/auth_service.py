from app.domain.interfaces.user_interface import UserRepository
from app.domain.interfaces.token_interface import TokenRepository, JWTRepository
from app.domain.interfaces.password_interface import PasswordHasher, PasswordValidator
from app.domain.interfaces.transaction_interface import TransactionManager
from app.domain.interfaces.link_interface import LinkDecoder
from app.application.dtos.user_dto import UserDTO
from app.domain.entities.user import User
from uuid import uuid4
from datetime import datetime
from typing import Callable, Optional
from uuid import UUID


class AuthService:
    def __init__(
        self,
        user_repository: UserRepository,
        token_repository: TokenRepository,
        jwt_repository: JWTRepository,
        password_hasher: PasswordHasher,
        password_validator: PasswordValidator,
        transaction_manager: TransactionManager,
        link_decoder: LinkDecoder,
    ):
        self.user_repo = user_repository
        self.token_repo = token_repository
        self.jwt_repository = jwt_repository
        self.password_hasher = password_hasher
        self.password_validator = password_validator
        self.transaction_manager = transaction_manager
        self.link_decoder = link_decoder

    async def register_user(
        self,
        email: str,
        username: str,
        password: str,
        send_email_func: Callable,
        base_url: str,
    ) -> UserDTO:

        await self._validate_registration(email, username, password)
        user_entity: User = self._create_user_entity(email, username, password)
        saved_entity: User = await self.user_repo.create(user_entity)
        token: str = self.token_repo.make_token(user_entity)

        self.transaction_manager.on_commit(
            lambda: send_email_func(str(user_entity.id), token, base_url=base_url)
        )
        return self._to_dto(saved_entity)

    async def verify_email(self, uidb64: str, token: str) -> UserDTO:
        user_id_str: str = self.link_decoder.decode(uidb64)
        user_id = UUID(user_id_str)
        user_entity: Optional[User] = await self.user_repo.get_by_id(user_id)

        if user_entity is None:
            raise ValueError("Пользователь не найден")

        self._validate_verify(user_entity)

        if not self.token_repo.check_token(user_entity, token):
            raise ValueError("Закончился срок действия токена")

        user_entity.email_confirmed = True
        updated_entity: Optional[User] = await self.user_repo.update(
            user_entity, update_fields=["email_confirmed"]
        )
        if updated_entity is None:
            raise ValueError("Пользователь не найден")

        return self._to_dto(updated_entity)

    async def login(self, login: str, password: str) -> dict[str, str]:
        user_entity = await self.user_repo.get_by_email(login)
        if not user_entity:
            user_entity = await self.user_repo.get_by_username(login)

        self._validate_login(user_entity, password)

        access_token = self.jwt_repository.create_access_token(user_entity)
        refresh_token = self.jwt_repository.create_refresh_token(user_entity)

        return {
            "access": access_token,
            "refresh": refresh_token,
            "token_type": "Bearer",
        }

    async def _validate_registration(
        self, email: str, username: str, password: str
    ) -> None:
        if await self.user_repo.get_by_email(email):
            raise ValueError("User with this email already exists")

        if await self.user_repo.get_by_username(username):
            raise ValueError("User with this username already exists")

        self.password_validator.validate(password)

    def _validate_verify(self, user_entity: Optional[User]) -> None:
        if not user_entity:
            raise ValueError("The user with this uuid was not found")
        if user_entity.email_confirmed:
            raise ValueError("Email уже подтвержден")

        self._chek_delete_or_block(user_entity)

    def _validate_login(self, user_entity: Optional[User], password: str):
        if not user_entity or not self.password_hasher.verify(
            password, user_entity.password_hash
        ):
            raise ValueError("Неверный логин или пароль")

        if not user_entity.email_confirmed:
            raise ValueError("Подтвердите email для входа")

        self._chek_delete_or_block(user_entity)

    def _chek_delete_or_block(self, user_entity: User) -> None:
        if not user_entity.is_active:
            raise ValueError("Аккаунт заблокирован")
        if user_entity.is_deleted:
            raise ValueError("Пользователь удален")

    def _create_user_entity(self, email: str, username: str, password: str) -> User:
        return User(
            id=uuid4(),
            email=email,
            username=username,
            password_hash=self.password_hasher.hash(password),
            created_at=datetime.now(),
        )

    def _to_dto(self, user_entity: User) -> UserDTO:
        return UserDTO(
            id=user_entity.id,
            email=user_entity.email,
            username=user_entity.username,
            email_confirmed=user_entity.email_confirmed,
        )
