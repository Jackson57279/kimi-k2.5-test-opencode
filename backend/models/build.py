"""Build model."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from models.base import BuildStatus, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from models.service import Service


class Build(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Build model."""

    __tablename__ = "builds"

    service_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("services.id", ondelete="CASCADE"), nullable=False, index=True
    )
    status: Mapped[BuildStatus] = mapped_column(
        String(20), default=BuildStatus.PENDING, nullable=False
    )
    commit_sha: Mapped[str | None] = mapped_column(String(40), nullable=True)
    commit_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    image_tag: Mapped[str | None] = mapped_column(String(255), nullable=True)
    logs: Mapped[str | None] = mapped_column(Text, nullable=True)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    duration_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)
    build_metadata: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    # Relationships
    service: Mapped["Service"] = relationship("Service", back_populates="builds")

    def __repr__(self) -> str:
        return f"<Build(id={self.id}, status={self.status})>"
