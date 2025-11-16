import uuid
from typing import Optional
from sqlalchemy import String, Boolean, Uuid, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from infrastructure.persistence.sqlalchemy.models.base import IsDeletedORM, Base


class ConflictItemORM(Base, IsDeletedORM):
    __tablename__ = "conflict_items"

    conflict_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("conflicts.id", ondelete="CASCADE"), nullable=False
    )

    title: Mapped[str] = mapped_column(String(100), nullable=False)

    creator_choice_value: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    partner_choice_value: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    agreed_choice_value: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    is_agreed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    conflict: Mapped["ConflictORM"] = relationship(
        "ConflictModel", back_populates="items", lazy="selectin"
    )
    events: Mapped[list["ConflictEventORM"]] = relationship(
        "ConflictEventModel", back_populates="item", lazy="selectin"
    )

    def __str__(self):
        return f"ConflictItemModel {self.id} for {self.conflict_id}"
