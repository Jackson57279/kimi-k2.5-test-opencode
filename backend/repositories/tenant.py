"""Tenant repository."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.tenant import Tenant
from repositories.base import BaseRepository


class TenantRepository(BaseRepository[Tenant]):
    """Repository for Tenant entities."""

    model = Tenant

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_by_slug(self, slug: str) -> Tenant | None:
        """Get tenant by slug."""
        query = select(Tenant).where(Tenant.slug == slug)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def slug_exists(self, slug: str) -> bool:
        """Check if a slug already exists."""
        tenant = await self.get_by_slug(slug)
        return tenant is not None
