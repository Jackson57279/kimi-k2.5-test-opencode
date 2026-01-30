"""Service repository."""

from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.base import ServiceStatus
from models.service import Service
from repositories.base import BaseRepository, PaginatedResult, PaginationParams, SortParams


class ServiceRepository(BaseRepository[Service]):
    """Repository for Service entities."""

    model = Service
    eager_load = ["builds", "environment_variables"]

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def list_by_project(
        self,
        project_id: str,
        status: ServiceStatus | None = None,
        pagination: PaginationParams | None = None,
        sort: SortParams | None = None,
    ) -> PaginatedResult[Service]:
        """List services for a specific project."""
        filters: dict[str, Any] = {"project_id": project_id}
        if status:
            filters["status"] = status
        return await self.list(filters=filters, pagination=pagination, sort=sort)

    async def get_by_name(self, name: str, project_id: str) -> Service | None:
        """Get service by name within a project."""
        query = select(Service).where(
            Service.name == name,
            Service.project_id == project_id,
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def list_by_status(
        self,
        status: ServiceStatus,
        pagination: PaginationParams | None = None,
        sort: SortParams | None = None,
    ) -> PaginatedResult[Service]:
        """List services by status."""
        filters: dict[str, Any] = {"status": status}
        return await self.list(filters=filters, pagination=pagination, sort=sort)

    async def update_status(self, service_id: str, status: ServiceStatus) -> Service:
        """Update service status."""
        return await self.update(service_id, {"status": status})

    async def get_running_services(
        self,
        pagination: PaginationParams | None = None,
    ) -> PaginatedResult[Service]:
        """Get all running services."""
        return await self.list_by_status(ServiceStatus.RUNNING, pagination=pagination)
