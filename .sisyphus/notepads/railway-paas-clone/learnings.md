# Railway PaaS Clone - Learnings & Conventions

## Project Conventions

### Directory Structure
- Monorepo with `backend/`, `frontend/`, `cli/` folders
- Single root git repository
- Docker Compose for PostgreSQL, Redis, Traefik only (not for app deployment)

### Technology Stack
- **Backend**: FastAPI + SQLAlchemy 2.0 (async) + Alembic + Celery + Redis
- **Frontend**: Next.js 14+ (App Router) + TypeScript + Tailwind + shadcn/ui
- **Process Management**: PM2 (no Docker for deployments)
- **Reverse Proxy**: Traefik with Let's Encrypt
- **Database**: PostgreSQL with asyncpg

### Design System (Railway Aesthetic)
- Background: slate-950 (#020617)
- Cards: bg-gray-900/80 with backdrop-blur-xl
- Gradients: indigo-600 to violet-600
- Accents: cyan-400, purple-500
- Typography: Inter/Geist for UI, JetBrains Mono for terminal

### Security Requirements
- AES-256-GCM for environment variable encryption (not Fernet)
- JWT with HTTP-only cookies (not localStorage)
- HMAC signature verification for webhooks
- RBAC with owner/admin/member roles

### Code Patterns
- Repository pattern for database access
- Pydantic v2 for validation
- Async/await throughout backend
- WebSocket with Redis pub/sub for scaling

## Task Execution Log

### Task 1: Project Structure & Monorepo Setup (COMPLETED)
- Created root directory structure: `backend/`, `frontend/`, `cli/`, `scripts/`, `docs/`
- Set up root `package.json` with npm workspaces for frontend and cli
- Created `docker-compose.yml` with PostgreSQL 15, Redis 7, and Traefik services
- Added comprehensive `.gitignore` covering Node, Python, Docker, IDE, and OS files
- Created `.editorconfig` for consistent code formatting across languages
- Wrote detailed `README.md` with setup instructions, architecture overview, and troubleshooting

### Key Decisions Made
1. **Workspace Structure**: Frontend and CLI in npm workspaces, backend separate (FastAPI)
2. **Docker Usage**: Only for dev dependencies (Postgres, Redis, Traefik), not for app deployment
3. **Package Manager**: Using npm with bun as specified
4. **Health Checks**: Added to all Docker services for reliability
5. **Network Isolation**: All services on internal `railway-network` bridge

### Files Created
- `package.json` - Root workspace configuration with dev scripts
- `docker-compose.yml` - Development services with persistent volumes
- `.gitignore` - Comprehensive ignore rules
- `.editorconfig` - Code style consistency
- `README.md` - Complete project documentation (284 lines)

