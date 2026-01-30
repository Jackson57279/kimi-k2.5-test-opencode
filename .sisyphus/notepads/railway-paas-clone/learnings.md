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


## Task 5: Redis & Celery Setup - Completed

### What Was Done
1. **Dependencies**: Updated backend/requirements.txt with Celery 5.6+, Redis client, and supporting packages
2. **Celery Configuration**: Created backend/celery_app.py with:
   - Redis broker and result backend (redis://localhost:6379/0)
   - JSON task serialization
   - Task time limits: 3600s hard, 3300s soft
   - Retry policy: max 3 retries with 60s delay
   - Queue routing: build, deploy, monitor, default queues
   - Worker prefetch multiplier: 1 (fair distribution)

3. **Example Tasks**: Created backend/tasks/example.py with:
   - add(): Simple addition task
   - long_running_task(): Simulates deployment/build (10s default)
   - process_deployment(): Full deployment workflow simulation
   - monitor_service(): Service health check simulation

4. **Testing**: Created backend/test_celery.py that verifies:
   - Task submission and execution
   - Result retrieval from Redis
   - Task status tracking
   - All example tasks working correctly

### Key Decisions
- Used Redis 7-alpine (already in docker-compose)
- JSON serialization for compatibility and debugging
- Prefetch multiplier = 1 for fair task distribution (no worker hoarding)
- Separate queues for different task types (build, deploy, monitor)
- Exponential backoff retry with 60s initial delay

### Verification Results
✅ Redis container running and healthy
✅ Celery worker starts successfully
✅ All example tasks execute and return results
✅ Task results stored in Redis
✅ Queue routing configured correctly

### Files Created/Modified
- backend/celery_app.py (new)
- backend/tasks/example.py (new)
- backend/tasks/__init__.py (updated)
- backend/requirements.txt (updated)
- backend/test_celery.py (new - for testing)

### Next Steps
- Integrate Celery with FastAPI endpoints
- Create deployment task that calls PM2
- Add WebSocket support for real-time task progress
- Implement task monitoring and logging

## Task 9: GitHub OAuth Authentication

### Patterns Used
- **AES-256-GCM encryption** for GitHub tokens via `cryptography` library
- **In-memory state storage** for OAuth CSRF protection with TTL-based expiration
- **Pydantic computed fields** for configuration validation (`github_oauth_configured`)
- **httpx async client** for GitHub API calls

### File Structure
- `config.py` - Settings including GitHub OAuth config
- `core/security.py` - Encryption utilities and JWT functions
- `services/github_oauth.py` - GitHub OAuth business logic
- `api/auth.py` - OAuth endpoints (/auth/github/login, /auth/github/callback)

### Key Decisions
- Used in-memory dict for OAuth state storage (sufficient for MVP, Redis recommended for production)
- State expires after 600 seconds (10 minutes)
- GitHub token stored encrypted in User model's `github_token_encrypted` field
- JWT tokens returned via redirect URL params to frontend


## Task 8: Repository Pattern Implementation - Learnings

### Patterns Used
- Generic BaseRepository[ModelType] using TypeVar for type-safe CRUD operations
- PaginationParams with capping (limit max 1000, min 1)
- SortParams with column introspection and safe fallback to created_at
- PaginatedResult container with has_more flag for UI pagination
- Custom exceptions: NotFoundError, ConflictError

### Repository Features Implemented
1. **BaseRepository** (7.7KB):
   - get_by_id, get_by_id_or_raise
   - list with filters, pagination, sorting
   - create, update, delete, delete_or_raise
   - exists, count helpers
   - Automatic eager loading via `eager_load` attribute

2. **Entity Repositories** (9 files):
   - TenantRepository: slug lookup
   - UserRepository: email/username lookup, tenant filtering, activate/deactivate/verify
   - ProjectRepository: tenant scoping, name uniqueness
   - ServiceRepository: status filtering, project scoping
   - BuildRepository: service scoping, status management, latest build helpers
   - TeamRepository: name lookup, member eager loading
   - TeamMemberRepository: team/user lookup, role management
   - EnvironmentVariableRepository: key lookup, upsert, bulk create
   - WebhookRepository: provider filtering, activate/deactivate

### Files Created
- `backend/models/base.py` - Mixins and enums
- `backend/models/tenant.py` - Tenant model
- `backend/models/user.py` - User model  
- `backend/models/project.py` - Project model
- `backend/models/service.py` - Service model
- `backend/models/build.py` - Build model
- `backend/models/team.py` - Team model
- `backend/models/team_member.py` - TeamMember model
- `backend/models/environment_variable.py` - EnvironmentVariable model
- `backend/models/webhook.py` - Webhook model
- `backend/models/__init__.py` - Model exports
- `backend/repositories/base.py` - BaseRepository and helpers
- `backend/repositories/tenant.py` - TenantRepository
- `backend/repositories/user.py` - UserRepository
- `backend/repositories/project.py` - ProjectRepository
- `backend/repositories/service.py` - ServiceRepository
- `backend/repositories/build.py` - BuildRepository
- `backend/repositories/team.py` - TeamRepository
- `backend/repositories/team_member.py` - TeamMemberRepository
- `backend/repositories/environment_variable.py` - EnvironmentVariableRepository
- `backend/repositories/webhook.py` - WebhookRepository
- `backend/repositories/__init__.py` - Repository exports
- `backend/tests/test_repositories.py` - Unit tests (29 tests)
- `backend/tests/conftest.py` - Pytest configuration

### Testing
- 29 tests pass
- Tests cover: pagination, sorting, errors, imports, enums

### Design Decisions
- All methods are async using AsyncSession
- Tenant isolation via tenant_id filters in relevant repositories
- Status enums stored as VARCHAR (not native enum) for flexibility
- Eager loading configurable per repository via class attribute
- Generic type system enables IDE autocompletion and type safety
