import uuid
from typing import Optional
from sqlalchemy import String, Text, Uuid, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from infrastructure.persistence.sqlalchemy.models.base import BaseORM, Base
from sqlalchemy import Enum as SQLEnum
import enum


class ProfileORM(Base, BaseORM):
    class GenderEnum(enum.Enum):
        NONE = ""
        MALE = "M"
        FEMALE = "F"

    __tablename__ = "profiles"

    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("users.id"), unique=True, nullable=False
    )

    first_name: Mapped[Optional[str]] = mapped_column(
        String(50), default="", nullable=True
    )
    last_name: Mapped[Optional[str]] = mapped_column(
        String(50), default="", nullable=True
    )
    # choices в Django реализуются как строковое поле с ограничениями на уровне приложения или БД
    gender: Mapped[Optional[GenderEnum]] = mapped_column(
        SQLEnum(GenderEnum), default="", nullable=True
    )  # 'M' или 'F'

    avatar_filename: Mapped[str] = mapped_column(
        String(255), default="avatars/default.jpg", nullable=False
    )

    location: Mapped[str] = mapped_column(String(30), default="", nullable=False)
    bio: Mapped[str] = mapped_column(Text, default="", nullable=False)

    # Связь: профиль принадлежит пользователю
    user: Mapped["UserORM"] = relationship(
        "UserModel", back_populates="profile", lazy="selectin"
    )

    def __str__(self):
        return f"Profile of {self.user.username if self.user else 'Unknown User'}"
