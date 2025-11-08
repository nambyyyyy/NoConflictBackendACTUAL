import enum
import uuid
from datetime import datetime
from typing import Optional, List
from sqlalchemy import (
    String,
    Float,
    DateTime,
    Boolean,
    Uuid,
    ForeignKey,
    Enum as SQLEnum,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from persistence.sqlalchemy.models.base import Base, IsDeletedORM


class ConflictORM(Base, IsDeletedORM):
    class ConflictStatusEnum(enum.Enum):
        PENDING = "pending"
        IN_PROGRESS = "in_progress"
        RESOLVED = "resolved"
        CANCELLED = "cancelled"
        ABANDONED = "abandoned"

    class TruceStatusEnum(enum.Enum):
        NONE = "none"
        PENDING = "pending"
        ACCEPTED = "accepted"

    __tablename__ = "conflicts"

    creator_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("users.id"), nullable=False
    )
    partner_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid, ForeignKey("users.id"), nullable=True
    )

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[ConflictStatusEnum] = mapped_column(
        SQLEnum(ConflictStatusEnum), default=ConflictStatusEnum.PENDING, nullable=False
    )
    slug: Mapped[Optional[str]] = mapped_column(String(255), unique=True, nullable=True)
    progress: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    deleted_by_creator: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    deleted_by_partner: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )

    truce_status: Mapped[TruceStatusEnum] = mapped_column(
        SQLEnum(TruceStatusEnum), default=TruceStatusEnum.NONE, nullable=False
    )

    truce_initiator_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        Uuid, ForeignKey("users.id"), nullable=True
    )

    creator: Mapped["UserORM"] = relationship(
        "UserModel",
        foreign_keys=[creator_id],
        back_populates="created_conflicts",
        lazy="joined",
    )
    partner: Mapped[Optional["UserORM"]] = relationship(
        "UserModel",
        foreign_keys=[partner_id],
        back_populates="partnered_conflicts",
        lazy="joined",
    )
    truce_initiator: Mapped[Optional["UserORM"]] = relationship(
        "UserModel",
        foreign_keys=[truce_initiator_id],
        back_populates="initiated_truces",
        lazy="joined",
    )
    items: Mapped[List["ConflictItemORM"]] = relationship(
        "ConflictItemModel", back_populates="conflict", lazy="joined"
    )
    events: Mapped[List["ConflictEventORM"]] = relationship(
        "ConflictEventModel", back_populates="conflict", lazy="joined"
    )
