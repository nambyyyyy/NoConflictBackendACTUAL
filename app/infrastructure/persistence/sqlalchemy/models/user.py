from sqlalchemy import Boolean, String, Index, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from persistence.sqlalchemy.models.base import Base, IsDeletedORM
from typing import Optional


class UserORM(Base, IsDeletedORM):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(
        String(30), unique=True, nullable=False, comment="Login"
    )
    email: Mapped[str] = mapped_column(
        String(254), unique=True, nullable=False, comment="Email address"
    )
    password: Mapped[str] = mapped_column(String, nullable=False, comment="Хеш пароля")
    email_confirmed: Mapped[bool] = mapped_column(
        Boolean, default=False, comment="Email подтвержден"
    )
    is_staff: Mapped[bool] = mapped_column(
        Boolean, default=False, comment="staff status"
    )
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, default=False, comment="superuser status"
    )
    is_god: Mapped[bool] = mapped_column(
        Boolean, default=False, comment="Создатель системы"
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, comment="active")
    
    profile: Mapped[Optional["ProfileORM"]] = relationship(
        "ProfileModel", back_populates="user", uselist=False, lazy="select"
    )
    created_conflicts: Mapped[list["ConflictORM"]] = relationship(
        "ConflictModel",
        back_populates="creator",
        foreign_keys="ConflictModel.creator_id", 
        lazy="select"
    )
    partnered_conflicts: Mapped[list["ConflictORM"]] = relationship(
        "ConflictModel",
        back_populates="partner",
        foreign_keys="ConflictModel.partner_id", 
        lazy="select"
    )
    initiated_truces: Mapped[list["ConflictORM"]] = relationship(
        "ConflictModel",
        back_populates="truce_initiator",
        foreign_keys="ConflictModel.truce_initiator_id", 
        lazy="select"
    )

    def __str__(self):
        return self.username

    __table_args__ = (
        Index("user_email_ci_idx", func.lower(email)),
        Index("user_username_ci_idx", func.lower(username)),
    )
