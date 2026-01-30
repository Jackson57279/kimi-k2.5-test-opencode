"""Base repository with common CRUD operations."""

from typing import Any, Generic, TypeVar, get_args

from sqlalchemy import asc, desc, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database import Base

ModelType = TypeVar("ModelType", bound=Base)


class NotFoundError(Exception):
    """Raised when an entity is not found."""

    def __init__(self, model_name: str, entity_id: str):
        self.model_name = model_name
        self.entity_id = entity_id
        super().__init__(f"{model_name} with id '{entity_id}' not found")


class ConflictError(Exception):
    """Raised when an entity already exists."""

    def __init__(self, message: str):
        super().__init__(message)


class PaginationParams:
    """Pagination parameters."""

    def __init__(self, skip: int = 0, limit: int = 100):
        self.skip = max(0, skip)
        self.limit = min(max(1, limit), 1000)  # Cap at 1000

    @property
    def offset(self) -> int:
        return self.skip


class SortParams:
    """Sort parameters."""

    def __init__(self, sort_by: str = "created_at", sort_order: str = "desc"):
        self.sort_by = sort_by
        self.sort_order = sort_order.lower() if sort_order else "desc"

    def apply(self, query: Any, model: type) -> Any:
        """Apply sorting to query."""
        column = getattr(model, self.sort_by, None)
        if column is None:
            column = getattr(model, "created_at", None)
        if column is not None:
            if self.sort_order == "asc":
                query = query.order_by(asc(column))
            else:
                query = query.order_by(desc(column))
        return query


class PaginatedResult(Generic[ModelType]):
    """Paginated result container."""

    def __init__(
        self,
        items: list[ModelType],
        total: int,
        skip: int,
        limit: int,
    ):
        self.items = items
        self.total = total
        self.skip = skip
        self.limit = limit
        self.has_more = skip + len(items) < total


class BaseRepository(Generic[ModelType]):
    """Base repository with async CRUD operations."""

    model: type[ModelType]
    eager_load: list[str] = []

    def __init__(self, session: AsyncSession):
        self.session = session

    def _get_model_class(self) -> type[ModelType]:
        """Get the model class from generic type."""
        if hasattr(self, "model"):
            return self.model
        # Fallback to introspection
        for base in type(self).__orig_bases__:  # type: ignore
            args = get_args(base)
            if args:
                return args[0]
        raise RuntimeError("Could not determine model type")

    def _apply_eager_loading(self, query: Any) -> Any:
        """Apply eager loading for relationships."""
        model_class = self._get_model_class()
        for attr_name in self.eager_load:
            attr = getattr(model_class, attr_name, None)
            if attr is not None:
                query = query.options(selectinload(attr))
        return query

    async def get_by_id(self, entity_id: str) -> ModelType | None:
        """Get an entity by ID."""
        model_class = self._get_model_class()
        query = select(model_class).where(model_class.id == entity_id)
        query = self._apply_eager_loading(query)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_id_or_raise(self, entity_id: str) -> ModelType:
        """Get an entity by ID or raise NotFoundError."""
        entity = await self.get_by_id(entity_id)
        if entity is None:
            model_class = self._get_model_class()
            raise NotFoundError(model_class.__name__, entity_id)
        return entity

    async def list(
        self,
        filters: dict[str, Any] | None = None,
        pagination: PaginationParams | None = None,
        sort: SortParams | None = None,
    ) -> PaginatedResult[ModelType]:
        """List entities with optional filtering, pagination, and sorting."""
        model_class = self._get_model_class()
        pagination = pagination or PaginationParams()
        sort = sort or SortParams()

        # Build base query
        query = select(model_class)

        # Apply filters
        if filters:
            for key, value in filters.items():
                if value is not None:
                    column = getattr(model_class, key, None)
                    if column is not None:
                        query = query.where(column == value)

        # Get total count
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.session.execute(count_query)
        total = total_result.scalar() or 0

        # Apply sorting
        query = sort.apply(query, model_class)

        # Apply pagination
        query = query.offset(pagination.offset).limit(pagination.limit)

        # Apply eager loading
        query = self._apply_eager_loading(query)

        # Execute query
        result = await self.session.execute(query)
        items = list(result.scalars().all())

        return PaginatedResult(
            items=items,
            total=total,
            skip=pagination.skip,
            limit=pagination.limit,
        )

    async def create(self, data: dict[str, Any]) -> ModelType:
        """Create a new entity."""
        model_class = self._get_model_class()
        try:
            entity = model_class(**data)
            self.session.add(entity)
            await self.session.flush()
            await self.session.refresh(entity)
            return entity
        except IntegrityError as e:
            await self.session.rollback()
            raise ConflictError(str(e.orig)) from e

    async def update(self, entity_id: str, data: dict[str, Any]) -> ModelType:
        """Update an entity by ID."""
        entity = await self.get_by_id_or_raise(entity_id)
        for key, value in data.items():
            if hasattr(entity, key) and value is not None:
                setattr(entity, key, value)
        await self.session.flush()
        await self.session.refresh(entity)
        return entity

    async def delete(self, entity_id: str) -> bool:
        """Delete an entity by ID."""
        entity = await self.get_by_id(entity_id)
        if entity is None:
            return False
        await self.session.delete(entity)
        await self.session.flush()
        return True

    async def delete_or_raise(self, entity_id: str) -> None:
        """Delete an entity by ID or raise NotFoundError."""
        entity = await self.get_by_id_or_raise(entity_id)
        await self.session.delete(entity)
        await self.session.flush()

    async def exists(self, entity_id: str) -> bool:
        """Check if an entity exists."""
        model_class = self._get_model_class()
        query = select(func.count()).where(model_class.id == entity_id)
        result = await self.session.execute(query)
        count = result.scalar() or 0
        return count > 0

    async def count(self, filters: dict[str, Any] | None = None) -> int:
        """Count entities with optional filtering."""
        model_class = self._get_model_class()
        query = select(func.count()).select_from(model_class)
        if filters:
            for key, value in filters.items():
                if value is not None:
                    column = getattr(model_class, key, None)
                    if column is not None:
                        query = query.where(column == value)
        result = await self.session.execute(query)
        return result.scalar() or 0
