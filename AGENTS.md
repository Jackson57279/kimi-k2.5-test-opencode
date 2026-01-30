# PROJECT KNOWLEDGE BASE

**Generated:** 2026-01-30
**Commit:** 9ac26b4
**Branch:** master

## OVERVIEW

Railway PaaS Clone — full-stack deployment platform with FastAPI backend, Next.js frontend, Celery workers, Traefik reverse proxy. Multi-tenant architecture with JWT auth.

## STRUCTURE

```
./
├── backend/          # FastAPI + SQLAlchemy + Celery (Python 3.11+)
├── frontend/         # Next.js 14 + Tailwind + shadcn/ui (TypeScript)
├── traefik/          # Reverse proxy config (Let's Encrypt, dynamic routing)
├── cli/              # Python CLI tool (empty/planned)
├── docs/             # Documentation (empty/planned)
├── scripts/          # Utility scripts
├── docker-compose.yml    # PostgreSQL 15 + Redis 7 + Traefik
├── ecosystem.config.js   # PM2 process manager config
└── package.json          # npm workspaces (frontend, cli)
```

## WHERE TO LOOK

| Task | Location | Notes |
|------|----------|-------|
| API endpoints | `backend/api/` | FastAPI routers, auth at `/auth` |
| Database models | `backend/models/` | SQLAlchemy 2.0, UUID PKs, tenant isolation |
| Data access | `backend/repositories/` | Generic CRUD + TenantRepository pattern |
| Background jobs | `backend/tasks/` | Celery tasks, `celery_app.py` config |
| Auth system | `backend/middleware/auth.py`, `backend/core/` | JWT + Redis blacklist |
| Frontend pages | `frontend/app/` | Next.js App Router |
| UI components | `frontend/components/ui/` | shadcn/ui (Radix primitives) |
| State management | `frontend/stores/` | Zustand stores |
| Reverse proxy | `traefik/dynamic/` | Dynamic service routing |

## COMMANDS

```bash
# Development
npm run docker:up          # Start PostgreSQL, Redis, Traefik
npm run dev                # Start frontend + backend concurrently

# Backend only
cd backend && python main.py                    # FastAPI on :8000
cd backend && celery -A celery_app worker       # Celery worker
cd backend && alembic upgrade head              # Run migrations

# Frontend only
cd frontend && bun dev     # Next.js on :3000

# Production (PM2)
pm2 start ecosystem.config.js --env production
```

## CONVENTIONS

- **Package manager**: bun for frontend, pip for backend
- **IDs**: UUID v4 strings (36 chars), never auto-increment
- **Async**: 100% async/await in backend, SQLAlchemy 2.0 style
- **Multi-tenancy**: All user data filtered by `tenant_id`
- **Imports**: Barrel exports via `__init__.py` in all packages

## ANTI-PATTERNS (THIS PROJECT)

- **NO** type suppressions (`as any`, `@ts-ignore`, `# type: ignore`)
- **NO** sync database operations — use async only
- **NO** direct model queries in API routes — use repositories
- **NO** hardcoded secrets — use `.env` files
- **NO** empty catch blocks

## UNIQUE STYLES

- Repository methods return `None` or raise `NotFoundError` (paired: `get_by_id` / `get_by_id_or_raise`)
- All API errors use `AppException` hierarchy with `to_dict()` serialization
- SQLAlchemy naming convention enforced for Alembic compatibility
- Celery tasks use automatic retry with exponential backoff + jitter

## ENVIRONMENT

```bash
# Required .env variables
DATABASE_URL=postgresql+asyncpg://...
REDIS_URL=redis://...
SECRET_KEY=...
JWT_SECRET_KEY=...

# Optional OAuth
GITHUB_CLIENT_ID=...
GITHUB_CLIENT_SECRET=...
```

## NOTES

- Frontend has `.next/` build artifacts — regenerate with `bun run build`
- Backend tests at `backend/tests/` — run with `pytest -v`
- Traefik uses staging ACME by default — switch to production for real certs
- PM2 ecosystem expects `logs/` directory at root
