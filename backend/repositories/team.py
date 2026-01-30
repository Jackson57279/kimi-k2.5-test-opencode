"""Team repository."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models.team import Team
from repositories.base import BaseRepository


class TeamRepository(BaseRepository[Team]):
    """Repository for Team entities."""

    model = Team
    eager_load = ["members"]

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_by_name(self, name: str) -> Team | None:
        """Get team by name."""
        query = select(Team).where(Team.name == name)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_with_members(self, team_id: str) -> Team | None:
        """Get team with all members loaded."""
        query = (
            select(Team)
            .where(Team.id == team_id)
            .options(selectinload(Team.members))
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def name_exists(self, name: str, exclude_id: str | None = None) -> bool:
        """Check if team name exists."""
        query = select(Team).where(Team.name == name)
        if exclude_id:
            query = query.where(Team.id != exclude_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none() is not None
