"""Team member repository."""

from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.base import TeamMemberRole
from models.team_member import TeamMember
from repositories.base import BaseRepository, PaginatedResult, PaginationParams, SortParams


class TeamMemberRepository(BaseRepository[TeamMember]):
    """Repository for TeamMember entities."""

    model = TeamMember

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def list_by_team(
        self,
        team_id: str,
        role: TeamMemberRole | None = None,
        pagination: PaginationParams | None = None,
        sort: SortParams | None = None,
    ) -> PaginatedResult[TeamMember]:
        """List team members for a specific team."""
        filters: dict[str, Any] = {"team_id": team_id}
        if role:
            filters["role"] = role
        return await self.list(filters=filters, pagination=pagination, sort=sort)

    async def list_by_user(
        self,
        user_id: str,
        pagination: PaginationParams | None = None,
        sort: SortParams | None = None,
    ) -> PaginatedResult[TeamMember]:
        """List team memberships for a specific user."""
        filters: dict[str, Any] = {"user_id": user_id}
        return await self.list(filters=filters, pagination=pagination, sort=sort)

    async def get_membership(self, team_id: str, user_id: str) -> TeamMember | None:
        """Get membership for a user in a team."""
        query = select(TeamMember).where(
            TeamMember.team_id == team_id,
            TeamMember.user_id == user_id,
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def is_member(self, team_id: str, user_id: str) -> bool:
        """Check if user is a member of team."""
        membership = await self.get_membership(team_id, user_id)
        return membership is not None

    async def has_role(self, team_id: str, user_id: str, role: TeamMemberRole) -> bool:
        """Check if user has a specific role in team."""
        membership = await self.get_membership(team_id, user_id)
        return membership is not None and membership.role == role

    async def update_role(self, team_id: str, user_id: str, role: TeamMemberRole) -> TeamMember:
        """Update a member's role in a team."""
        membership = await self.get_membership(team_id, user_id)
        if membership is None:
            from repositories.base import NotFoundError
            raise NotFoundError("TeamMember", f"{team_id}:{user_id}")
        return await self.update(membership.id, {"role": role})

    async def remove_member(self, team_id: str, user_id: str) -> bool:
        """Remove a member from a team."""
        membership = await self.get_membership(team_id, user_id)
        if membership is None:
            return False
        await self.session.delete(membership)
        await self.session.flush()
        return True
