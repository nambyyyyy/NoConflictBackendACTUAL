import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import DateTime, Boolean, Uuid, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Базовый класс для всех моделей."""

    pass


class BaseORM:
    """
    Абстрактная базовая модель, содержащая поля id, created_at, updated_at.
    """

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid, primary_key=True, default=uuid.uuid4, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False
    )


class IsDeletedORM(BaseORM):
    """
    Абстрактная модель, расширяющая BaseModel, добавляющая поля для мягкого удаления.
    """

    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
