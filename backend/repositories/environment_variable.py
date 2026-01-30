"""Environment variable repository."""

from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.environment_variable import EnvironmentVariable
from repositories.base import BaseRepository, PaginatedResult, PaginationParams, SortParams


class EnvironmentVariableRepository(BaseRepository[EnvironmentVariable]):
    """Repository for EnvironmentVariable entities."""

    model = EnvironmentVariable

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def list_by_service(
        self,
        service_id: str,
        is_secret: bool | None = None,
        pagination: PaginationParams | None = None,
        sort: SortParams | None = None,
    ) -> PaginatedResult[EnvironmentVariable]:
        """List environment variables for a specific service."""
        filters: dict[str, Any] = {"service_id": service_id}
        if is_secret is not None:
            filters["is_secret"] = is_secret
        return await self.list(filters=filters, pagination=pagination, sort=sort)

    async def get_by_key(self, service_id: str, key: str) -> EnvironmentVariable | None:
        """Get environment variable by key for a service."""
        query = select(EnvironmentVariable).where(
            EnvironmentVariable.service_id == service_id,
            EnvironmentVariable.key == key,
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def key_exists(self, service_id: str, key: str, exclude_id: str | None = None) -> bool:
        """Check if key exists for service."""
        query = select(EnvironmentVariable).where(
            EnvironmentVariable.service_id == service_id,
            EnvironmentVariable.key == key,
        )
        if exclude_id:
            query = query.where(EnvironmentVariable.id != exclude_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none() is not None

    async def upsert(
        self,
        service_id: str,
        key: str,
        value: str,
        is_secret: bool = False,
    ) -> EnvironmentVariable:
        """Create or update an environment variable."""
        existing = await self.get_by_key(service_id, key)
        if existing:
            return await self.update(existing.id, {"value": value, "is_secret": is_secret})
        return await self.create({
            "service_id": service_id,
            "key": key,
            "value": value,
            "is_secret": is_secret,
        })

    async def delete_by_key(self, service_id: str, key: str) -> bool:
        """Delete environment variable by key."""
        env_var = await self.get_by_key(service_id, key)
        if env_var is None:
            return False
        await self.session.delete(env_var)
        await self.session.flush()
        return True

    async def bulk_create(
        self,
        service_id: str,
        variables: list[dict[str, Any]],
    ) -> list[EnvironmentVariable]:
        """Bulk create environment variables for a service."""
        created = []
        for var in variables:
            env_var = await self.create({
                "service_id": service_id,
                "key": var["key"],
                "value": var["value"],
                "is_secret": var.get("is_secret", False),
            })
            created.append(env_var)
        return created
