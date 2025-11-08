import enum
import uuid
from typing import Optional
from sqlalchemy import (
    Text,
    Uuid,
    ForeignKey,
    Enum as SQLEnum,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from persistence.sqlalchemy.models.base import Base, IsDeletedORM


class ConflictEventORM(Base, IsDeletedORM):
    class EventTypeEnum(enum.Enum):
        TRUCE_OFFER = "truce_offer"
        TRUCE_ACCEPTED = "truce_accepted"
        TRUCE_DECLINED = "truce_declined"
        CONFLICT_DELETE = "conflict_delete"
        CONFLICT_CANCEL = "conflict_cancel"
        CONFLICT_RESOLVED = "conflict_resolved"
        ITEM_AGREED = "item_agreed"
        ITEM_ADD = "item_add"
        ITEM_UPDATE = "item_update"
        CONFLICT_JOIN_SUCCESS = "conflict_join_success"
        CONFLICT_CREATE = "conflict_create"

    __tablename__ = "conflict_events"

    conflict_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("conflicts.id", ondelete="CASCADE"), nullable=False
    )
    item_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid, ForeignKey("conflict_items.id", ondelete="CASCADE"), nullable=True
    )
    initiator_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid, ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    event_type: Mapped[EventTypeEnum] = mapped_column(
        SQLEnum(EventTypeEnum), nullable=False
    )

    old_value: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    new_value: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    conflict: Mapped["ConflictORM"] = relationship(
        "ConflictORM", back_populates="events", lazy="select"
    )
    item: Mapped[Optional["ConflictItemORM"]] = relationship(
        "ConflictItemORM", back_populates="events", lazy="select"
    )
    initiator: Mapped[Optional["UserORM"]] = relationship("UserORM", lazy="joined")
