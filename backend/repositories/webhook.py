"""Webhook repository."""

from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.base import WebhookProvider
from models.webhook import Webhook
from repositories.base import BaseRepository, PaginatedResult, PaginationParams, SortParams


class WebhookRepository(BaseRepository[Webhook]):
    """Repository for Webhook entities."""

    model = Webhook

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def list_by_service(
        self,
        service_id: str,
        provider: WebhookProvider | None = None,
        is_active: bool | None = None,
        pagination: PaginationParams | None = None,
        sort: SortParams | None = None,
    ) -> PaginatedResult[Webhook]:
        """List webhooks for a specific service."""
        filters: dict[str, Any] = {"service_id": service_id}
        if provider:
            filters["provider"] = provider
        if is_active is not None:
            filters["is_active"] = is_active
        return await self.list(filters=filters, pagination=pagination, sort=sort)

    async def get_by_url(self, url: str) -> Webhook | None:
        """Get webhook by URL."""
        query = select(Webhook).where(Webhook.url == url)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def list_active_by_service(
        self,
        service_id: str,
        pagination: PaginationParams | None = None,
    ) -> PaginatedResult[Webhook]:
        """List active webhooks for a service."""
        return await self.list_by_service(
            service_id=service_id,
            is_active=True,
            pagination=pagination,
        )

    async def activate(self, webhook_id: str) -> Webhook:
        """Activate a webhook."""
        return await self.update(webhook_id, {"is_active": True})

    async def deactivate(self, webhook_id: str) -> Webhook:
        """Deactivate a webhook."""
        return await self.update(webhook_id, {"is_active": False})
