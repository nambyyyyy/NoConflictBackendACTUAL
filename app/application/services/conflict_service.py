from domain.interfaces.conflict_interface import (
    ConflictRepository,
)
from domain.interfaces.item_interface import ItemRepository
from domain.interfaces.event_interface import EventRepository
from domain.entities.conflict import Conflict, ConflictError, ConflictStatusEnum, TruceStatusEnum
from domain.entities.conflict_item import ConflictItem
from domain.entities.conflict_event import ConflictEvent, EventType
from application.validators.conflict_validators import ConflictValidator
from typing import Optional, Callable
from uuid import UUID, uuid4
from datetime import datetime, timezone


class ConflictService:
    def __init__(
        self,
        conflict_repository: ConflictRepository,
        item_repository: ItemRepository,
        event_repository: EventRepository,
    ):
        self.conflict_repo = conflict_repository
        self.item_repo = item_repository
        self.event_repo = event_repository
        self.conflict_valid = ConflictValidator()

    async def create_conflict(
        self,
        creator_id: UUID,
        partner_id: Optional[UUID],
        title: str,
        items: list[dict],
    ) -> Conflict:

        self.conflict_valid.validate_conflict_registration(
            creator_id, partner_id, title, items
        )

        conflict_entity: Conflict = Conflict.create_entity( # type: ignore
            title=title,
            id=uuid4(),
            creator_id=creator_id,
            slug=str(uuid4()),
        )

        items_entitys: list[ConflictItem] = [
            ConflictItem.create_entity(
                id=uuid4(),  # type: ignore
                conflict_id=conflict_entity.id,
                title=item.get("title"),  # type: ignore
                creator_choice_value=item.get("creator_choice_value"),
            )
            for item in items
        ]
        
        events_entitys: list[ConflictEvent] = [
            ConflictEvent.create_entity(
                id=uuid4(),
                conflict_id=conflict_entity.id,
                event_type=EventType.CONFLICT_CREATE,
                initiator_id=conflict_entity.creator_id,
                initiator_username=conflict_entity.creator_username,
            )
        ]

        for item in items_entitys:
            events_entitys.append(
                ConflictEvent.create_entity(
                    id=uuid4(),
                    conflict_id=conflict_entity.id,
                    event_type=EventType.ITEM_ADD,
                    initiator_id=conflict_entity.creator_id,
                    initiator_username=conflict_entity.creator_username,
                    item_id=item.id,
                    item_title=item.title,
                    new_value=item.creator_choice_value
                )
            )

        await self.conflict_repo.create(conflict_entity)
        
        for item in items_entitys:
            await self.item_repo.create(item)
         
        for event in events_entitys:
            await self.event_repo.create(event)


        conflict_entity: Optional[Conflict] = await self.conflict_repo.get_by_id(
            conflict_entity.id
        )
        if conflict_entity is None:
            raise ConflictError("Conflict not created")

        return conflict_entity

    async def get_conflict(self, user_id: UUID, slug: str) -> Optional[Conflict]:
        conflict_entity: Optional[Conflict] = await self.conflict_repo.get_by_slug(slug)
        self.conflict_valid.validate_access_conflict(conflict_entity, user_id)
        self.conflict_valid.validate_delete_conflict(conflict_entity, user_id)  # type: ignore
        return conflict_entity

    async def cancel_conflict(
        self,
        user_id: UUID,
        slug: str,
        channel_layer: Callable,
    ) -> Conflict:
        conflict_entity: Optional[Conflict] = await self.conflict_repo.get_by_slug(slug)
        self.conflict_valid.validate_access_conflict(conflict_entity, user_id)

        event_entity: ConflictEvent = ConflictEvent.create_entity(
            id=uuid4(),
            conflict_id=conflict_entity.id,
            event_type=EventType.CONFLICT_CANCEL,
            created_at=datetime.now(timezone.utc),
            initiator_id=user_id,
            initiator_username=(
                conflict_entity.creator_username
                if conflict_entity.partner_username == user_id
                else conflict_entity.partner_username
            ),
        )
        await self.event_repo.create(event_entity)

        conflict_entity.status = ConflictStatusEnum.CANCELLED
        conflict_entity.resolved_at = datetime.now(timezone.utc)

        updated_conflict: Conflict = await self.conflict_repo.update(
            conflict_entity, update_fields=["status", "resolved_at"]  # type: ignore
        )  # type: ignore

        # await channel_layer().group_send(
        #     f"conflict_{slug}",
        #     {
        #         "type": "conflict.cancelled",
        #         "status": "cancelled",
        #         "progress": saved_conflict.progress,
        #         "resolved_at": saved_conflict.resolved_at.isoformat(),  # type: ignore
        #         "initiator_id": event_entity.initiator_id,
        #         "initiator_username": event_entity.initiator_username,
        #     },
        # )
        return updated_conflict

    async def delete_conflict(self, user_id: UUID, slug: str) -> None:
        conflict_entity: Optional[Conflict] = await self.conflict_repo.get_by_slug(slug)
        self.conflict_valid.validate_access_conflict(conflict_entity, user_id)
        self.conflict_valid.validate_delete_conflict(conflict_entity, user_id)  # type: ignore

        if user_id == conflict_entity.creator_id:
            conflict_entity.deleted_by_creator = True

        elif user_id == conflict_entity.partner_id:
            conflict_entity.deleted_by_partner = True

        if conflict_entity.deleted_by_creator and conflict_entity.deleted_by_partner:
            conflict_entity.is_deleted = True
            conflict_entity.resolved_at = datetime.now(timezone.utc)

        await self.conflict_repo.update(
            conflict_entity,
            update_fields=[
                "deleted_by_creator",
                "deleted_by_partner",
                "is_deleted",
                "resolved_at",
            ],
            return_none=True,
        )

    async def create_offer_truce(
        self,
        user_id: UUID,
        slug: str,
        channel_layer: Callable,
    ) -> Conflict:
        return await self._update_offer_truce(
            user_id, slug, channel_layer, TruceStatusEnum.NONE, TruceStatusEnum.PENDING
        )

    async def cancel_offer_truce(
        self,
        user_id: UUID,
        slug: str,
        channel_layer: Callable,
    ) -> Conflict:
        return await self._update_offer_truce(
            user_id, slug, channel_layer, TruceStatusEnum.PENDING, TruceStatusEnum.NONE
        )

    async def accepted_offer_truce(
        self,
        user_id: UUID,
        slug: str,
        channel_layer: Callable,
    ) -> Conflict:
        return await self._update_offer_truce(
            user_id, slug, channel_layer, TruceStatusEnum.PENDING, TruceStatusEnum.ACCEPTED
        )

    async def update_item(
        self,
        event_type: EventType,
        user_id: UUID,
        slug: str,
        item_id: UUID,
        item_title: str,
        new_value: str,
    ) -> Conflict | ConflictItem:
        self.conflict_valid.validate_item_update(
            event_type, user_id, slug, item_id, new_value
        )
        conflict_entity: Optional[Conflict] = await self.conflict_repo.get_by_slug(slug)
        self.conflict_valid.validate_access_conflict(conflict_entity, user_id)

        item: Optional[ConflictItem] = await self.item_repo.get_by_id_and_conflict_id(
            item_id, conflict_entity.id
        )

        if item is None:
            raise ConflictError("Item Not Found")

        if user_id == conflict_entity.creator_id:
            old_value = item.creator_choice_value
            item.creator_choice_value = new_value
        else:
            old_value = item.partner_choice_value
            item.partner_choice_value = new_value

        event_entity: ConflictEvent = ConflictEvent.create_entity(
            id=uuid4(),
            conflict_id=conflict_entity.id,
            event_type=event_type,
            initiator_id=(
                conflict_entity.creator_id
                if conflict_entity.creator_id == user_id
                else conflict_entity.partner_id
            ),
            initiator_username=(
                conflict_entity.creator_username
                if conflict_entity.creator_id == user_id
                else conflict_entity.partner_username
            ),
            item_id=item_id,
            item_title=item_title,
            old_value=old_value,
            new_value=new_value,
        )

        await self.event_repo.create(event_entity)

        if (item.creator_choice_value and item.partner_choice_value) and (
            item.creator_choice_value == item.partner_choice_value
        ):
            item.agreed_choice_value = item.creator_choice_value
            item.is_agreed = True

            self._update_progress(conflict_entity, item.id)
            event_entity: ConflictEvent = ConflictEvent.create_entity(
                id=uuid4(),
                conflict_id=conflict_entity.id,
                event_type=EventType.CONFLICT_RESOLVED,
            )
            await self.event_repo.create(event_entity)
            conflict: Conflict = await self.conflict_repo.update(
                conflict_entity, update_fields=["progress", "status", "resolved_at"]
            )  # type: ignore

        await self.item_repo.update(
            item,
            update_fields=[
                "creator_choice_value",
                "partner_choice_value",
                "agreed_choice_value",
                "is_agreed",
            ],
        )
        return conflict if item.is_agreed else item

    async def _update_offer_truce(
        self,
        user_id: UUID,
        slug: str,
        channel_layer: Callable,
        old_truce_status: TruceStatusEnum,
        new_truce_status: TruceStatusEnum,
    ) -> Conflict:
        conflict_entity: Optional[Conflict] = await self.conflict_repo.get_by_slug(slug)
        self.conflict_valid.validate_access_conflict(conflict_entity, user_id)

        event_entity: ConflictEvent = ConflictEvent.create_entity(
            id=uuid4(),
            conflict_id=conflict_entity.id,
            event_type=EventType.TRUCE_OFFER,
            created_at=datetime.now(timezone.utc),
            initiator_id=user_id,
            initiator_username=(
                conflict_entity.creator_username
                if conflict_entity.creator_id == user_id
                else conflict_entity.partner_username
            ),
            old_value=old_truce_status,
            new_value=new_truce_status,
        )
        await self.event_repo.create(event_entity)

        conflict_entity.truce_status = new_truce_status
        conflict_entity.truce_initiator_id = user_id
        conflict_entity.truce_initiator_username = (
            conflict_entity.creator_username
            if user_id == conflict_entity.creator_id
            else conflict_entity.partner_username
        )
        saved_conflict: Conflict = await self.conflict_repo.update(
            conflict_entity,
            update_fields=[
                "truce_status",
                "truce_initiator_id",
            ],
        )

        return saved_conflict

    def _update_progress(self, conflict: Conflict, item_id: UUID) -> None:
        for index, item in enumerate(conflict.items):
            if item.id == item_id:
                conflict.items[index] = item
                break

        total_items = len(conflict.items)
        agreed_count = sum(1 for item in conflict.items if item.is_agreed)
        conflict.progress = (
            round((agreed_count / total_items) * 100, 2) if total_items else 0.0
        )
        if conflict.progress >= 100:
            conflict.status = ConflictStatusEnum.RESOLVED
            conflict.resolved_at = datetime.now(timezone.utc)
