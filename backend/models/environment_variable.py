"""Environment variable model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from models.base import TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from models.service import Service


class EnvironmentVariable(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Environment variable model."""

    __tablename__ = "environment_variables"
    __table_args__ = (
        Index("ix_env_vars_service_key", "service_id", "key", unique=True),
    )

    service_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("services.id", ondelete="CASCADE"), nullable=False
    )
    key: Mapped[str] = mapped_column(String(255), nullable=False)
    value: Mapped[str] = mapped_column(Text, nullable=False)
    is_secret: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Relationships
    service: Mapped["Service"] = relationship("Service", back_populates="environment_variables")

    def __repr__(self) -> str:
        return f"<EnvironmentVariable(service_id={self.service_id}, key={self.key})>"
