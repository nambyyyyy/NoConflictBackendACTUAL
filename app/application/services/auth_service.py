from domain.interfaces.user_interface import UserRepository
from domain.interfaces.token_interface import EmailTokenRepository, JWTRepository
from domain.interfaces.password_interface import PasswordHasher, PasswordValidator
from domain.interfaces.link_interface import LinkDecoder
from domain.entities.user import User
from typing import Callable, Optional
from datetime import datetime
from uuid import UUID, uuid4
from application.validators.auth_validators import AuthValidator


class AuthService:
    def __init__(
        self,
        user_repository: UserRepository,
        email_token_repository: EmailTokenRepository,
        jwt_repository: JWTRepository,
        password_hasher: PasswordHasher,
        password_validator: PasswordValidator,
        link_decoder: LinkDecoder,
    ):
        self.user_repo = user_repository
        self.email_token_repository = email_token_repository
        self.jwt_repository = jwt_repository
        self.password_hasher = password_hasher
        self.password_validator = password_validator
        self.link_decoder = link_decoder
        self.validator = AuthValidator(
            self.user_repo, self.password_hasher, self.password_validator
        )

    async def register_user(
        self,
        email: str,
        username: str,
        password: str,
        send_email_func: Callable,
        base_url: str,
    ) -> User:

        await self.validator.validate_registration(email, username, password)
        user_entity: User = User.create_entity(
            id=uuid4(),
            email=email,
            username=username,
            password_hash=self.password_hasher.hash(password),
            created_at=datetime.now(),
        )
        saved_entity: User = await self.user_repo.create(user_entity)
        token: str = self.email_token_repository.generate_token(str(user_entity.id))

        send_email_func(str(saved_entity.id), token, base_url=base_url)
        return saved_entity

    async def verify_email(self, uidb64: str, token: str) -> User:
        user_id: str = self.link_decoder.decode(uidb64)
        user_entity: Optional[User] = await self.user_repo.get_by_id(UUID(user_id))

        if user_entity is None:
            raise ValueError("Пользователь не найден")

        self.validator.validate_verify(user_entity)

        if not self.email_token_repository.verify_token(token):
            raise ValueError("Закончился срок действия токена")

        user_entity.email_confirmed = True
        updated_entity: Optional[User] = await self.user_repo.update(
            user_entity, update_fields=["email_confirmed"]
        )
        if updated_entity is None:
            raise ValueError("Пользователь не найден")

        return updated_entity

    async def login(self, login: str, password: str) -> dict[str, str]:
        user_entity: Optional[User] = await self.user_repo.get_by_email(login)
        if not user_entity:
            user_entity = await self.user_repo.get_by_username(login)

        self.validator.validate_login(user_entity, password)

        access_token = self.jwt_repository.create_access_token(user_entity) # type: ignore
        refresh_token = self.jwt_repository.create_refresh_token(user_entity) # type: ignore

        return {
            "access": access_token,
            "refresh": refresh_token,
            "token_type": "Bearer",
        }
