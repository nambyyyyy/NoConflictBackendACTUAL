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
from infrastructure.persistence.sqlalchemy.models.base import BaseORM, Base



class ConflictEventORM(Base, BaseORM):
    class EventTypeEnum(enum.Enum):
        TRUCE_OFFER = "TRUCE_OFFER"
        TRUCE_ACCEPTED = "TRUCE_ACCEPTED"
        TRUCE_DECLINED = "TRUCE_DECLINED"
        CONFLICT_DELETE = "CONFLICT_DELETE"
        CONFLICT_CANCEL = "CONFLICT_CANCEL"
        CONFLICT_RESOLVED = "CONFLICT_RESOLVED"
        ITEM_AGREED = "ITEM_AGREED"
        ITEM_ADD = "ITEM_ADD"
        ITEM_UPDATE = "ITEM_UPDATE"
        CONFLICT_JOIN_SUCCESS = "CONFLICT_JOIN_SUCCESS"
        CONFLICT_CREATE = "CONFLICT_CREATE"
        
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
        SQLEnum(
            EventTypeEnum,
            name="eventtypeenum",
        ),
        nullable=False,
    )
    old_value: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    new_value: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    conflict: Mapped["ConflictORM"] = relationship(
        "ConflictORM", back_populates="events", lazy="selectin"
    )
    item: Mapped[Optional["ConflictItemORM"]] = relationship(
        "ConflictItemORM", back_populates="events", lazy="selectin"
    )
    initiator: Mapped[Optional["UserORM"]] = relationship("UserORM", lazy="selectin")
