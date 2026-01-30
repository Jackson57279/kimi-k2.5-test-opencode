"""Team member model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from models.base import TeamMemberRole, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from models.team import Team
    from models.user import User


class TeamMember(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Team member model."""

    __tablename__ = "team_members"
    __table_args__ = (
        Index("ix_team_members_team_user", "team_id", "user_id", unique=True),
    )

    team_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("teams.id", ondelete="CASCADE"), nullable=False
    )
    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    role: Mapped[TeamMemberRole] = mapped_column(
        String(20), default=TeamMemberRole.MEMBER, nullable=False
    )

    # Relationships
    team: Mapped["Team"] = relationship("Team", back_populates="members")
    user: Mapped["User"] = relationship("User", back_populates="team_memberships")

    def __repr__(self) -> str:
        return f"<TeamMember(team_id={self.team_id}, user_id={self.user_id}, role={self.role})>"
