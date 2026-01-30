"""Build repository."""

from datetime import datetime
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.base import BuildStatus
from models.build import Build
from repositories.base import BaseRepository, PaginatedResult, PaginationParams, SortParams


class BuildRepository(BaseRepository[Build]):
    """Repository for Build entities."""

    model = Build

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def list_by_service(
        self,
        service_id: str,
        status: BuildStatus | None = None,
        pagination: PaginationParams | None = None,
        sort: SortParams | None = None,
    ) -> PaginatedResult[Build]:
        """List builds for a specific service."""
        filters: dict[str, Any] = {"service_id": service_id}
        if status:
            filters["status"] = status
        return await self.list(filters=filters, pagination=pagination, sort=sort)

    async def list_by_status(
        self,
        status: BuildStatus,
        pagination: PaginationParams | None = None,
        sort: SortParams | None = None,
    ) -> PaginatedResult[Build]:
        """List builds by status."""
        filters: dict[str, Any] = {"status": status}
        return await self.list(filters=filters, pagination=pagination, sort=sort)

    async def get_latest_build(self, service_id: str) -> Build | None:
        """Get the latest build for a service."""
        query = (
            select(Build)
            .where(Build.service_id == service_id)
            .order_by(Build.created_at.desc())
            .limit(1)
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_latest_successful_build(self, service_id: str) -> Build | None:
        """Get the latest successful build for a service."""
        query = (
            select(Build)
            .where(
                Build.service_id == service_id,
                Build.status == BuildStatus.SUCCESS,
            )
            .order_by(Build.created_at.desc())
            .limit(1)
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def update_status(
        self,
        build_id: str,
        status: BuildStatus,
        logs: str | None = None,
    ) -> Build:
        """Update build status and optionally logs."""
        data: dict[str, Any] = {"status": status}
        if logs is not None:
            data["logs"] = logs
        return await self.update(build_id, data)

    async def start_build(self, build_id: str) -> Build:
        """Mark build as started."""
        return await self.update(
            build_id,
            {"status": BuildStatus.BUILDING, "started_at": datetime.utcnow()},
        )

    async def complete_build(
        self,
        build_id: str,
        success: bool,
        logs: str | None = None,
        image_tag: str | None = None,
    ) -> Build:
        """Complete a build with success or failure."""
        finished_at = datetime.utcnow()
        build = await self.get_by_id_or_raise(build_id)
        
        duration = None
        if build.started_at:
            duration = int((finished_at - build.started_at).total_seconds())
        
        data: dict[str, Any] = {
            "status": BuildStatus.SUCCESS if success else BuildStatus.FAILED,
            "finished_at": finished_at,
            "duration_seconds": duration,
        }
        if logs is not None:
            data["logs"] = logs
        if image_tag is not None:
            data["image_tag"] = image_tag
        
        return await self.update(build_id, data)

    async def get_pending_builds(
        self,
        pagination: PaginationParams | None = None,
    ) -> PaginatedResult[Build]:
        """Get pending builds."""
        return await self.list_by_status(BuildStatus.PENDING, pagination=pagination)
