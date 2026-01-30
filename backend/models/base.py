"""Common model utilities, mixins, and enums."""

import enum
from datetime import datetime
from typing import Any
from uuid import uuid4

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column


def generate_uuid() -> str:
    """Generate a UUID string for primary keys."""
    return str(uuid4())


class TimestampMixin:
    """Mixin for created_at and updated_at timestamps."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        onupdate=func.now(),
        nullable=True,
    )


class UUIDPrimaryKeyMixin:
    """Mixin for UUID string primary keys."""

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=generate_uuid,
    )


# Enums for model fields


class UserRole(str, enum.Enum):
    """User roles within a tenant."""

    OWNER = "owner"
    ADMIN = "admin"
    MEMBER = "member"


class ServiceStatus(str, enum.Enum):
    """Service deployment status."""

    PENDING = "pending"
    BUILDING = "building"
    RUNNING = "running"
    FAILED = "failed"
    STOPPED = "stopped"


class BuildStatus(str, enum.Enum):
    """Build status."""

    PENDING = "pending"
    BUILDING = "building"
    SUCCESS = "success"
    FAILED = "failed"


class WebhookProvider(str, enum.Enum):
    """Webhook providers."""

    GITHUB = "github"


class TeamMemberRole(str, enum.Enum):
    """Team member roles."""

    OWNER = "owner"
    ADMIN = "admin"
    MEMBER = "member"
