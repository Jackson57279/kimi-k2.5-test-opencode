"""Webhook model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from models.base import TimestampMixin, UUIDPrimaryKeyMixin, WebhookProvider

if TYPE_CHECKING:
    from models.service import Service


class Webhook(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Webhook model."""

    __tablename__ = "webhooks"

    service_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("services.id", ondelete="CASCADE"), nullable=False, index=True
    )
    provider: Mapped[WebhookProvider] = mapped_column(
        String(20), default=WebhookProvider.GITHUB, nullable=False
    )
    secret: Mapped[str] = mapped_column(String(255), nullable=False)
    url: Mapped[str] = mapped_column(String(500), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    service: Mapped["Service"] = relationship("Service", back_populates="webhooks")

    def __repr__(self) -> str:
        return f"<Webhook(id={self.id}, provider={self.provider})>"
