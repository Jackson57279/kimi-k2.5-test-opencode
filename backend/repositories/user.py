"""User repository."""

from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User
from repositories.base import BaseRepository, PaginatedResult, PaginationParams, SortParams


class UserRepository(BaseRepository[User]):
    """Repository for User entities."""

    model = User

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_by_email(self, email: str, tenant_id: str | None = None) -> User | None:
        """Get user by email, optionally filtered by tenant."""
        query = select(User).where(User.email == email)
        if tenant_id:
            query = query.where(User.tenant_id == tenant_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_username(self, username: str, tenant_id: str | None = None) -> User | None:
        """Get user by username, optionally filtered by tenant."""
        query = select(User).where(User.username == username)
        if tenant_id:
            query = query.where(User.tenant_id == tenant_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def list_by_tenant(
        self,
        tenant_id: str,
        is_active: bool | None = None,
        pagination: PaginationParams | None = None,
        sort: SortParams | None = None,
    ) -> PaginatedResult[User]:
        """List users for a specific tenant."""
        filters: dict[str, Any] = {"tenant_id": tenant_id}
        if is_active is not None:
            filters["is_active"] = is_active
        return await self.list(filters=filters, pagination=pagination, sort=sort)

    async def email_exists(self, email: str, tenant_id: str, exclude_id: str | None = None) -> bool:
        """Check if email exists in tenant, optionally excluding a specific user."""
        query = select(User).where(User.email == email, User.tenant_id == tenant_id)
        if exclude_id:
            query = query.where(User.id != exclude_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none() is not None

    async def activate(self, user_id: str) -> User:
        """Activate a user."""
        return await self.update(user_id, {"is_active": True})

    async def deactivate(self, user_id: str) -> User:
        """Deactivate a user."""
        return await self.update(user_id, {"is_active": False})

    async def verify(self, user_id: str) -> User:
        """Mark user as verified."""
        return await self.update(user_id, {"is_verified": True})
