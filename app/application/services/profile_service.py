from app.domain.interfaces.profile_interface import ProfileRepository
from app.domain.interfaces.avatar_processor import AvatarProcessor
from uuid import UUID, uuid4
from typing import Optional
from app.domain.entities.profile import Profile
from application.dtos.profile_dto import ProfileDTO
from datetime import datetime


class ProfileService:
    def __init__(
        self,
        profile_repository: ProfileRepository,
        avatar_processor: AvatarProcessor,
        media_base_url: str,
    ):
        self.media_base_url = media_base_url
        self.profile_repo = profile_repository
        self.avatar_processor = avatar_processor

    async def create_profile(self, user_id: UUID) -> ProfileDTO:
        if await self.profile_repo.get_by_user_id(user_id):
            raise ValueError("Profile already exists")

        profile_entity: Profile = Profile.create_entity(id=uuid4(), user_id=user_id)
        created_profile: Profile = await self.profile_repo.create(profile_entity)
        return ProfileDTO.create_dto(created_profile)

    async def update_profile(
        self,
        user_id: UUID,
        profile_data: dict,
        avatar_file: Optional[object] = None,
    ) -> ProfileDTO:

        profile_entity: Optional[Profile] = await self.profile_repo.get_by_user_id(
            user_id
        )

        if profile_entity is None:
            raise ValueError("Profile not found")

        if avatar_file is not None:
            profile_entity.avatar_filename = await self.avatar_processor.process_avatar(
                avatar_file, user_id
            )

        for field_name, field_value in profile_data.items():
            setattr(profile_entity, field_name, field_value)

        profile_entity: Optional[Profile] = await self.profile_repo.update(
            profile_entity
        )
        if profile_entity is None:
            raise ValueError("Profile not found")

        return ProfileDTO.create_dto(profile_entity)

    # def _get_avatar_url(self, filename: Optional[str]) -> Optional[str]:
    #     return f"{self.media_base_url}avatars/{filename}" if filename else None

    # def _get_fullname(self, first_name: Optional[str], last_name: Optional[str]):
    #     return (
    #         f"{first_name} {last_name}".strip() if (first_name and last_name) else None
    #     )


