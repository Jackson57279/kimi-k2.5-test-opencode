# BACKEND KNOWLEDGE BASE

## OVERVIEW

FastAPI async backend with SQLAlchemy 2.0, multi-tenant architecture, JWT auth with Redis blacklist, Celery task queue.

## STRUCTURE

```
backend/
├── api/              # FastAPI routers (auth, services, projects)
├── core/             # Security utilities (JWT, cookies, encryption)
├── middleware/       # Auth middleware, exception handlers
├── models/           # SQLAlchemy models (9 entities + base mixins)
├── repositories/     # Data access layer (BaseRepository + TenantRepository)
├── schemas/          # Pydantic v2 request/response models
├── services/         # External integrations (GitHub OAuth, token blacklist)
├── tasks/            # Celery background tasks
├── tests/            # pytest test suite
├── main.py           # FastAPI app entry point
├── database.py       # Async SQLAlchemy config
├── celery_app.py     # Celery worker config
└── config.py         # Pydantic Settings
```

## WHERE TO LOOK

| Task | Location | Notes |
|------|----------|-------|
| Add API endpoint | `api/__init__.py` | Include router in `v1_router` |
| Add model | `models/` | Inherit `UUIDPrimaryKeyMixin`, `TimestampMixin` |
| Add repository | `repositories/` | Extend `BaseRepository` or `TenantRepository` |
| Auth logic | `middleware/auth.py` | `get_current_user`, `require_role()` |
| JWT operations | `core/jwt.py` | `JWTService` with Redis blacklist |
| Background job | `tasks/` | Decorate with `@celery_app.task` |
| Config value | `config.py` | Add to `Settings` class |

## LAYER PATTERN

```
API (api/)
  ↓ calls
Repositories (repositories/)
  ↓ queries
Models (models/)
  ↓ mapped to
Database (database.py)
```

**Note**: Service layer (`services/`) is for external integrations only — business logic lives in API endpoints.

## REPOSITORY PATTERN

```python
# BaseRepository provides async CRUD
class UserRepository(TenantRepository[User]):
    model = User
    
    async def get_by_email(self, email: str) -> User | None:
        query = select(User).where(User.email == email)
        # TenantRepository auto-injects: .where(User.tenant_id == self.tenant_id)
```

**Three tenant isolation strategies:**
1. **Direct**: Entity has `tenant_id` (User, Project)
2. **Owner-based**: Join through User table (Team)
3. **Chain-based**: Multi-hop joins (Service→Project, Build→Service→Project)

## CONVENTIONS

- **Pagination**: `PaginationParams(skip=0, limit=100)`, max 1000
- **Sorting**: `SortParams(sort_by="created_at", sort_order="desc")`
- **Filtering**: Dict with `{"column": value}` or `{"column": [list]}`
- **Eager loading**: Set `eager_load = ["relationship"]` on repository class
- **Session**: Passed to repository constructor, not managed by repository

## ANTI-PATTERNS

- **NO** `session.commit()` in repositories — handled by FastAPI dependency
- **NO** raw SQL queries — use SQLAlchemy select()
- **NO** sync database drivers — use `asyncpg` only
- **NO** catching generic `Exception` — use specific types
- **NO** `# TODO` without ticket reference

## MODEL CONVENTIONS

```python
class MyModel(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "my_models"
    
    # Foreign keys with cascade delete
    tenant_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("tenants.id", ondelete="CASCADE")
    )
    
    # Relationships with selectin loading
    children: Mapped[list["Child"]] = relationship(
        "Child", back_populates="parent", lazy="selectin", cascade="all, delete-orphan"
    )
```

## EXCEPTION HIERARCHY

```
AppException (base)
├── NotFoundError (404)
├── ValidationError (422)
├── AuthenticationError (401)
├── AuthorizationError (403)
├── ConflictError (409)
├── BadRequestError (400)
└── InternalServerError (500)
```

All exceptions have `.to_dict()` for JSON serialization and are auto-logged.

## CELERY TASKS

```python
@celery_app.task(
    bind=True,
    queue="deployment",  # deployment | build | cleanup | default
    max_retries=3,
)
def my_task(self, arg):
    # Auto-retry on failure with exponential backoff
    pass
```

## NOTES

- Run migrations before starting: `alembic upgrade head`
- Health check: `GET /health` returns `{"status": "healthy"}`
- API docs: `GET /docs` (disabled in production)
- Debug mode auto-creates tables (dev only)
