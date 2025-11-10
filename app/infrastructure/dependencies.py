from app.infrastructure.persistence.sqlalchemy.repositories.user_repository import (
    SQLAlchemyUserRepository,
)

from backend.app.infrastructure.security.token_repository import (
    FastAPIEmailTokenRepository,
    FastAPIJWTRepository,
)
from app.infrastructure.persistence.sqlalchemy.repositories.profile_repository import (
    SQLAlchemyProfileRepository,
)
from app.infrastructure.persistence.sqlalchemy.repositories.conflict_repository import (
    SQLAlchemyConflictRepository,
)
from app.infrastructure.persistence.sqlalchemy.repositories.item_repository import (
    SQLAlchemyConflictItemRepository,
)
from app.infrastructure.persistence.sqlalchemy.repositories.event_repository import (
    SQLAlchemyConflictEventRepository,
)
from app.infrastructure.persistence.sqlalchemy.repositories.conflict_repository import (
    SQLAlchemyConflictRepository,
)
from app.infrastructure.persistence.sqlalchemy.repositories.item_repository import (
    SQLAlchemyConflictItemRepository,
)
from app.infrastructure.persistence.sqlalchemy.repositories.event_repository import (
    SQLAlchemyConflictEventRepository,
)

from app.infrastructure.security.password_hasher import FastAPIPasswordHasher
from app.infrastructure.security.password_validator import FastAPIPasswordValidator
from app.infrastructure.security.link_decoder import FastAPILinkDecoder
from app.application.services.auth_service import AuthService
from app.application.services.profile_service import ProfileService
from app.application.services.conflict_service import ConflictService

from app.infrastructure.database.sessions import get_db_session

# from app.no_conflict_project.settings import SECRET_KEY, MEDIA_URL
# from app.infrastructure.processors.avatar.avatar_processor import DjangoAvatarProcessor
# from app.infrastructure.processors.avatar.avatar_validator import AvatarValidator
# from app.infrastructure.processors.avatar.filename_generator import FilenameGenerator
# from app.infrastructure.processors.avatar.image_processor import ImageProcessor
# from app.infrastructure.processors.avatar.image_saver import ImageSaver
# from app.infrastructure.storage.local_storage import LocalStorage
import os
from dotenv import load_dotenv
load_dotenv()


async def get_auth_service() -> AuthService:
    """Фабрика для создания AuthService"""
    return AuthService(
        user_repository=SQLAlchemyUserRepository(await get_db_session()),
        email_token_repository=FastAPIEmailTokenRepository(os.getenv("SECRET_KEY")),
        jwt_repository=FastAPIJWTRepository(
            secret_key=os.getenv("SECRET_KEY"), algorithm="HS256"
        ),
        password_hasher=FastAPIPasswordHasher(),
        password_validator=FastAPIPasswordValidator(),
        link_decoder=FastAPILinkDecoder(),
    )


def get_profile_service() -> ProfileService:
    """Фабрика для создания ProfileService"""
    # avatar_processor = DjangoAvatarProcessor(
    #     validator=AvatarValidator(),
    #     generator=FilenameGenerator(),
    #     processor=ImageProcessor(),
    #     saver=ImageSaver(storage=LocalStorage()),
    #     upload_dir="avatars",
    # )

    return ProfileService(
        profile_repository=SQLAlchemyProfileRepository(),
        # avatar_processor=avatar_processor,
        # media_base_url=MEDIA_URL,
    )


async def get_conflict_service() -> ConflictService:
    """Фабрика для создания ConflictService"""
    return ConflictService(
        conflict_repository=SQLAlchemyConflictRepository(await get_db_session()),
        item_repository=SQLAlchemyConflictItemRepository(await get_db_session()),
        event_repository=SQLAlchemyConflictEventRepository(await get_db_session()),
    )
