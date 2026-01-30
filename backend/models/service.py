"""Service model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from models.base import ServiceStatus, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from models.build import Build
    from models.environment_variable import EnvironmentVariable
    from models.project import Project
    from models.webhook import Webhook


class Service(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Service model."""

    __tablename__ = "services"
    __table_args__ = (
        Index("ix_services_project_name", "project_id", "name"),
    )

    project_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[ServiceStatus] = mapped_column(
        String(20), default=ServiceStatus.PENDING, nullable=False
    )
    git_repo: Mapped[str | None] = mapped_column(String(500), nullable=True)
    git_branch: Mapped[str] = mapped_column(String(255), default="main", nullable=False)
    dockerfile_path: Mapped[str] = mapped_column(String(255), default="Dockerfile", nullable=False)
    build_context: Mapped[str] = mapped_column(String(255), default=".", nullable=False)
    port: Mapped[int | None] = mapped_column(Integer, nullable=True)
    domain: Mapped[str | None] = mapped_column(String(255), nullable=True)
    image: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # Relationships
    project: Mapped["Project"] = relationship("Project", back_populates="services")
    builds: Mapped[list["Build"]] = relationship(
        "Build", back_populates="service", lazy="selectin", cascade="all, delete-orphan"
    )
    environment_variables: Mapped[list["EnvironmentVariable"]] = relationship(
        "EnvironmentVariable", back_populates="service", lazy="selectin", cascade="all, delete-orphan"
    )
    webhooks: Mapped[list["Webhook"]] = relationship(
        "Webhook", back_populates="service", lazy="selectin", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Service(id={self.id}, name={self.name}, status={self.status})>"
