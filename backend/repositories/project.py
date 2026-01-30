"""Project repository."""

from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.project import Project
from repositories.base import BaseRepository, PaginatedResult, PaginationParams, SortParams


class ProjectRepository(BaseRepository[Project]):
    """Repository for Project entities."""

    model = Project
    eager_load = ["services"]

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def list_by_tenant(
        self,
        tenant_id: str,
        pagination: PaginationParams | None = None,
        sort: SortParams | None = None,
    ) -> PaginatedResult[Project]:
        """List projects for a specific tenant."""
        filters: dict[str, Any] = {"tenant_id": tenant_id}
        return await self.list(filters=filters, pagination=pagination, sort=sort)

    async def get_by_name(self, name: str, tenant_id: str) -> Project | None:
        """Get project by name within a tenant."""
        query = select(Project).where(
            Project.name == name,
            Project.tenant_id == tenant_id,
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def name_exists(self, name: str, tenant_id: str, exclude_id: str | None = None) -> bool:
        """Check if project name exists in tenant."""
        query = select(Project).where(
            Project.name == name,
            Project.tenant_id == tenant_id,
        )
        if exclude_id:
            query = query.where(Project.id != exclude_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none() is not None
