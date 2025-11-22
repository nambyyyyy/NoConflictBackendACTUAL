from infrastructure.persistence.sqlalchemy.repositories.user_repository import (
    SQLAlchemyUserRepository,
)

from infrastructure.security.token_repository import (
    FastAPIEmailTokenRepository,
    FastAPIJWTRepository,
)
from infrastructure.persistence.sqlalchemy.repositories.profile_repository import (
    SQLAlchemyProfileRepository,
)
from infrastructure.persistence.sqlalchemy.repositories.conflict_repository import (
    SQLAlchemyConflictRepository,
)
from infrastructure.persistence.sqlalchemy.repositories.item_repository import (
    SQLAlchemyConflictItemRepository,
)
from infrastructure.persistence.sqlalchemy.repositories.event_repository import (
    SQLAlchemyConflictEventRepository,
)
from infrastructure.persistence.sqlalchemy.repositories.conflict_repository import (
    SQLAlchemyConflictRepository,
)
from infrastructure.persistence.sqlalchemy.repositories.item_repository import (
    SQLAlchemyConflictItemRepository,
)
from infrastructure.persistence.sqlalchemy.repositories.event_repository import (
    SQLAlchemyConflictEventRepository,
)
from infrastructure.persistence.sqlalchemy.repositories.user_repository import (
    SQLAlchemyUserRepository,
)

from infrastructure.security.password_hasher import FastAPIPasswordHasher
from infrastructure.security.password_validator import FastAPIPasswordValidator
from infrastructure.security.link_decoder import FastAPILinkDecoder
from application.services.auth_service import AuthService

from application.services.profile_service import ProfileService
from application.services.conflict_service import ConflictService
from application.services.user_service import UserService
from domain.entities.conflict_item import ConflictItem
from domain.entities.conflict_event import ConflictEvent
from domain.entities.conflict import Conflict
from domain.entities.user import User
from domain.entities.profile import Profile
from infrastructure.database.sessions import get_db_session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
import jwt
from dotenv import load_dotenv
from uuid import UUID
import os
from sqlalchemy.ext.asyncio import AsyncSession

# from app.no_conflict_project.settings import SECRET_KEY, MEDIA_URL
# from domain.infrastructure.processors.avatar.avatar_processor import DjangoAvatarProcessor
# from app.infrastructure.processors.avatar.avatar_validator import AvatarValidator
# from app.infrastructure.processors.avatar.filename_generator import FilenameGenerator
# from app.infrastructure.processors.avatar.image_processor import ImageProcessor
# from app.infrastructure.processors.avatar.image_saver import ImageSaver
# from app.infrastructure.storage.local_storage import LocalStorage


load_dotenv()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/login")



async def get_auth_service(
    session: AsyncSession = Depends(get_db_session),
) -> AuthService:
    return AuthService(
        user_repository=SQLAlchemyUserRepository(session, User),
        email_token_repository=FastAPIEmailTokenRepository(os.getenv("SECRET_KEY")),
        jwt_repository=FastAPIJWTRepository(
            secret_key=os.getenv("SECRET_KEY"), algorithm="HS256"
        ),
        password_hasher=FastAPIPasswordHasher(),
        password_validator=FastAPIPasswordValidator(),
        link_decoder=FastAPILinkDecoder(),
    )


async def get_conflict_service(
    session: AsyncSession = Depends(get_db_session),
) -> ConflictService:
    return ConflictService(
        conflict_repository=SQLAlchemyConflictRepository(session, Conflict),
        item_repository=SQLAlchemyConflictItemRepository(session, ConflictItem),
        event_repository=SQLAlchemyConflictEventRepository(
            session, entity=ConflictEvent
        ),
    )


async def get_user_service(
    session: AsyncSession = Depends(get_db_session),
) -> UserService:
    return UserService(user_repository=SQLAlchemyUserRepository(session, User))


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_service: UserService = Depends(get_user_service),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await user_service.get_user(UUID(user_id))
    if user is None:
        raise credentials_exception
    return user


async def get_profile_service(
    session: AsyncSession = Depends(get_db_session),
) -> ProfileService:
    return ProfileService(
        profile_repository=SQLAlchemyProfileRepository(session, Profile)
        
    )