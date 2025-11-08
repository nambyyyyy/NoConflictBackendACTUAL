from app.infrastructure.persistence.sqlalchemy.repositories.user_repository import (
    SQLAlchemyUserRepository,
)

# from infrastructure.persistence.token_repository import (
#     DjangoTokenRepository,
#     DjangoJWTRepository,
# )
from app.infrastructure.persistence.sqlalchemy.repositories.profile_repository import (
    SQLAlchemyProfileRepository,
)

# from app.infrastructure.persistence.transaction_manager import DjangoTransactionManager
from app.infrastructure.persistence.sqlalchemy.repositories.conflict_repository import (
    SQLAlchemyConflictRepository,
)
from app.infrastructure.persistence.sqlalchemy.repositories.item_repository import (
    SQLAlchemyConflictItemRepository,
)
from app.infrastructure.persistence.sqlalchemy.repositories.event_repository import (
    SQLAlchemyConflictEventRepository,
)
from app.infrastructure.persistence.sqlalchemy.repositories.conflict_repository import SQLAlchemyConflictRepository
from app.infrastructure.persistence.sqlalchemy.repositories.item_repository import SQLAlchemyConflictItemRepository
from app.infrastructure.persistence.sqlalchemy.repositories.event_repository import SQLAlchemyConflictEventRepository

# from app.infrastructure.security.django_password_hasher import DjangoPasswordHasher
# from app.infrastructure.security.django_password_validator import DjangoPasswordValidator
# from app.infrastructure.security.django_link_decoder import DjangoLinkDecoder
from app.application.services.auth_service import AuthService
from app.application.services.profile_service import ProfileService
from app.application.services.conflict_service import ConflictService

from app.infrastructure.database.dependencies import get_db_session

# from app.no_conflict_project.settings import SECRET_KEY, MEDIA_URL
# from app.infrastructure.processors.avatar.avatar_processor import DjangoAvatarProcessor
# from app.infrastructure.processors.avatar.avatar_validator import AvatarValidator
# from app.infrastructure.processors.avatar.filename_generator import FilenameGenerator
# from app.infrastructure.processors.avatar.image_processor import ImageProcessor
# from app.infrastructure.processors.avatar.image_saver import ImageSaver
# from app.infrastructure.storage.local_storage import LocalStorage


def get_auth_service() -> AuthService:
    """Фабрика для создания AuthService"""
    return AuthService(
        user_repository=SQLAlchemyUserRepository(),
        # token_repository=DjangoTokenRepository(),
        # jwt_repository=DjangoJWTRepository(secret_key=SECRET_KEY, algorithm="HS256"),
        # password_hasher=DjangoPasswordHasher(),
        # password_validator=DjangoPasswordValidator(),
        # transaction_manager=DjangoTransactionManager(),
        # link_decoder=DjangoLinkDecoder(),
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
