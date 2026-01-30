# Railway PaaS Clone - Production MVP Work Plan

## TL;DR

> **Build a full-stack Railway.com PaaS clone** with PM2 process-based deployments, GitHub OAuth, real-time log streaming, team workspaces, and Railway aesthetic UI. Production-ready MVP with SSL, resource quotas, email notifications, and comprehensive CLI.
>
> **Deliverables**: 
> - Backend: FastAPI + PostgreSQL + Redis + Celery
> - Frontend: Next.js 14+ with glassmorphism UI
> - CLI: Full deployment management tool
> - Infrastructure: PM2 process orchestration + Traefik reverse proxy
>
> **Estimated Effort**: Large (120-150 hours across 40+ tasks)
> **Parallel Execution**: YES - 5 major waves with 60% parallelization potential
> **Critical Path**: Setup → Database → Auth → Core API → Frontend Shell → Integration

---

## Context

### Original Request
Build a comprehensive Railway.com PaaS clone with full-stack implementation including Git-based deployments, real-time logs, team workspaces, and production-grade infrastructure.

### Interview Summary
**Key Discussions**:
- Infrastructure: Process-based deployment via PM2 (no Docker)
- Git providers: GitHub only for MVP
- Auth: GitHub OAuth + team invitation system
- Stack: FastAPI + Next.js + PostgreSQL + Redis
- Testing: Comprehensive TDD approach
- Timeline: Production MVP scope

**User Confirmed Scope**:
- **INCLUDE**: All core PaaS features, SSL certificates, resource quotas, email notifications, CLI tool, Railway aesthetic UI
- **EXCLUDE**: Multi-region, auto-scaling, custom domains, billing integration, GitLab/Bitbucket support, multiple database types

### Research Findings
**Architecture Patterns from Coolify/Dokploy/Dokku**:
- Queue-based deployments (Celery/BullMQ) with timeout handling
- Multi-tenant database design with RLS policies
- WebSocket streaming with Redis pub/sub for scaling
- PM2 programmatic API for process management
- Traefik dynamic configuration for SSL/routing
- AES-256-GCM encryption for secrets (superior to Fernet)

**Technical Decisions**:
- Repository pattern for data access with SQLAlchemy 2.0
- Async FastAPI with Uvicorn
- Next.js 14 App Router with Tailwind CSS
- Celery + Redis for background jobs
- WebSocket ConnectionManager with heartbeat
- RLS policies for multi-tenant security

---

## Work Objectives

### Core Objective
Build a production-grade Railway.com PaaS clone enabling developers to deploy applications via Git push, manage services through a glassmorphism dashboard, collaborate in team workspaces, and monitor deployments with real-time logs.

### Concrete Deliverables
1. **Backend API** (`backend/` folder)
   - FastAPI application with async endpoints
   - SQLAlchemy 2.0 models with Alembic migrations
   - WebSocket server for real-time log streaming
   - Celery workers for background jobs
   - GitHub OAuth integration
   - PM2 process management service
   - Email notification service (Resend)

2. **Frontend Dashboard** (`frontend/` folder)
   - Next.js 14+ App Router application
   - Railway aesthetic UI (slate-950, glassmorphism, indigo-violet gradients)
   - Real-time log viewer with WebSocket client
   - Service management interface
   - Team workspace management
   - Project creation and configuration

3. **CLI Tool** (`cli/` folder)
   - Python CLI for local deployment management
   - Configuration file handling
   - Log streaming from PM2 processes
   - Project scaffolding commands

4. **Infrastructure**
   - PostgreSQL database with multi-tenant schema
   - Redis for queues and caching
   - PM2 ecosystem configuration
   - Traefik reverse proxy setup
   - Let's Encrypt SSL automation

### Definition of Done
- [ ] User can sign up/login with GitHub OAuth
- [ ] User can create projects and connect GitHub repositories
- [ ] User can deploy services (PM2 processes) with one click
- [ ] Real-time build logs stream via WebSocket
- [ ] Environment variables encrypted and injectable
- [ ] Team members can be invited with RBAC roles
- [ ] Services auto-restart on failure with health checks
- [ ] GitHub webhooks trigger automatic deployments
- [ ] SSL certificates auto-provisioned via Let's Encrypt
- [ ] Resource quotas enforced (CPU/memory limits)
- [ ] Email notifications sent on deployment failures
- [ ] CLI tool supports local deployment management

### Must Have (Non-Negotiable)
- PM2-based process deployment (no Docker)
- GitHub OAuth authentication
- WebSocket real-time log streaming
- Encrypted environment variables
- Team workspaces with RBAC
- SSL certificate automation
- Service health monitoring
- Background job processing (Celery)
- Railway aesthetic UI implementation
- Comprehensive test coverage

### Must NOT Have (Guardrails)
- Docker containerization (explicitly excluded)
- Kubernetes orchestration
- Multi-region deployment
- Auto-scaling based on metrics
- Custom domain support (post-MVP)
- Billing/stripe integration
- GitLab/Bitbucket support
- Multiple database types (MySQL, MongoDB)
- Cron job services
- Serverless functions

---

## Verification Strategy

### Test Infrastructure Setup

**Test Decision**:
- **Infrastructure exists**: NO (starting from scratch)
- **User wants tests**: YES - Comprehensive TDD
- **Framework**: 
  - Backend: pytest with async support
  - Frontend: Vitest + React Testing Library
  - E2E: Playwright

**Test Setup Task**:
- [ ] 0.1 Setup Backend Test Infrastructure
  - Install: `pip install pytest pytest-asyncio pytest-cov httpx`
  - Config: Create `backend/pytest.ini` with asyncio_mode=auto
  - Verify: `cd backend && pytest --version` → pytest 7.x+ shows
  - Example: Create `backend/tests/conftest.py` with fixtures
  - Verify: `cd backend && pytest tests/` → 0 tests collected (infrastructure ready)

- [ ] 0.2 Setup Frontend Test Infrastructure
  - Install: `cd frontend && bun add -d vitest @testing-library/react @testing-library/jest-dom jsdom @vitejs/plugin-react`
  - Config: Create `frontend/vitest.config.ts` with jsdom environment
  - Verify: `cd frontend && bun vitest --version` → vitest 1.x+ shows
  - Example: Create `frontend/src/components/__tests__/example.test.tsx`
  - Verify: `cd frontend && bun vitest run` → 1 test passes

### Automated Verification (Agent-Executable)

**Backend Verification Pattern**:
```bash
# For each API endpoint task:
curl -s -X POST http://localhost:8000/api/v1/projects \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"test-project"}' \
  | jq '.id'
# Assert: Returns non-empty UUID
# Assert: HTTP status 201

# For WebSocket verification:
bun -e "
const WebSocket = require('ws');
const ws = new WebSocket('ws://localhost:8000/ws/logs?serviceId=test&token=$TOKEN');
ws.on('open', () => console.log('Connected'));
ws.on('message', (data) => console.log('Received:', data.toString()));
setTimeout(() => ws.close(), 5000);
"
# Assert: "Connected" appears in output
# Assert: Log messages received within 5 seconds
```

**Frontend Verification Pattern** (using Playwright):
```bash
# Agent executes via playwright browser automation:
1. Navigate to: http://localhost:3000/login
2. Click: "Sign in with GitHub" button
3. Wait for redirect to GitHub OAuth
4. Mock GitHub callback with test token
5. Wait for: selector ".dashboard-container" to be visible
6. Assert: URL is "/dashboard"
7. Screenshot: .sisyphus/evidence/auth-success.png

# For real-time log viewer:
1. Navigate to: http://localhost:3000/services/test-service
2. Click: "Logs" tab
3. Wait for: WebSocket connection indicator green
4. Assert: Log entries appear within 10 seconds
5. Screenshot: .sisyphus/evidence/log-streaming.png
```

**CLI Verification Pattern**:
```bash
# Agent runs:
railway-cli deploy --project test-project --service test-service
# Assert: Exit code 0
# Assert: Output contains "Deployment successful"

railway-cli logs --service test-service --follow=false --lines=50
# Assert: Exit code 0
# Assert: Output contains log lines
```

**Integration Verification Pattern**:
```bash
# Full deployment flow test:
1. Create project via API
2. Connect GitHub repo
3. Trigger deployment via webhook
4. Verify PM2 process started
5. Verify logs stream via WebSocket
6. Verify health check passes
7. Stop service and verify cleanup
```

---

## Execution Strategy

### Parallel Execution Waves

```
WAVE 1: Foundation (Independent Setup Tasks)
├── Task 1: Project Structure & Monorepo Setup
├── Task 2: Backend Dependencies & FastAPI Setup
├── Task 3: Frontend Dependencies & Next.js Setup
├── Task 4: Database Setup (PostgreSQL)
├── Task 5: Redis & Celery Setup
└── Task 6: Traefik & PM2 Setup

WAVE 2: Backend Core (After Wave 1)
├── Task 7: SQLAlchemy Models & Alembic
├── Task 8: Repository Pattern Implementation
├── Task 9: GitHub OAuth Authentication
├── Task 10: JWT Token Management
├── Task 11: Core API Endpoints (Projects, Services)
└── Task 12: Error Handling & Pydantic Validation

WAVE 3: Frontend Core (After Wave 1)
├── Task 13: Tailwind Config & Design System
├── Task 14: shadcn/ui Components Setup
├── Task 15: Authentication UI (Login, Callback)
├── Task 16: Dashboard Layout & Navigation
├── Task 17: Project Management UI
└── Task 18: Service Management UI

WAVE 4: Advanced Features (After Waves 2 & 3)
├── Task 19: WebSocket Log Streaming (Backend)
├── Task 20: WebSocket Client (Frontend)
├── Task 21: PM2 Process Management Service
├── Task 22: Git-based Deployment Pipeline
├── Task 23: Environment Variable Encryption
├── Task 24: Team Workspaces & RBAC
├── Task 25: Webhook Handlers
└── Task 26: Background Jobs (Celery)

WAVE 5: Production & Polish (After Wave 4)
├── Task 27: SSL Certificate Automation
├── Task 28: Resource Monitoring & Analytics
├── Task 29: Email Notifications (Resend)
├── Task 30: Health Checks & Auto-restart
├── Task 31: Database Backup System
├── Task 32: CLI Tool Implementation
├── Task 33: Cost Estimation Display
├── Task 34: E2E Testing Suite
├── Task 35: Performance Optimization
└── Task 36: Documentation

CRITICAL PATH: 1 → 2 → 4 → 7 → 9 → 11 → 19 → 21 → 22 → 30 → 34
PARALLEL SPEEDUP: ~55% faster than sequential (can run 3-4 tasks in parallel during Waves 1-3)
```

### Dependency Matrix

| Task | Depends On | Blocks | Can Parallelize With |
|------|------------|--------|---------------------|
| 1 (Structure) | None | 2, 3 | 4, 5, 6 |
| 2 (Backend Setup) | 1 | 7, 8, 9 | 3, 4, 5, 6 |
| 3 (Frontend Setup) | 1 | 13, 14, 15 | 2, 4, 5, 6 |
| 4 (Database) | 1 | 7, 8 | 2, 3, 5, 6 |
| 5 (Redis/Celery) | 1 | 26 | 2, 3, 4, 6 |
| 6 (Traefik/PM2) | 1 | 21, 27, 28 | 2, 3, 4, 5 |
| 7 (Models) | 2, 4 | 8, 11, 24 | 9, 10 |
| 8 (Repository) | 7 | 11, 23 | 9, 10 |
| 9 (OAuth) | 2 | 10, 15, 24 | 7, 8 |
| 10 (JWT) | 9 | 11, 15, 19, 25 | 7, 8 |
| 11 (Core API) | 7, 8, 10 | 19, 21, 22 | 12 |
| 12 (Validation) | 2 | 11 | 11 |
| 13 (Tailwind) | 3 | 14, 16 | 15, 17, 18 |
| 14 (shadcn/ui) | 13 | 16, 17, 18 | 15 |
| 15 (Auth UI) | 3, 10 | 16 | 13, 14 |
| 16 (Dashboard) | 13, 14, 15 | 17, 18 | None |
| 17 (Project UI) | 16 | 20 | 18 |
| 18 (Service UI) | 16 | 20 | 17 |
| 19 (WebSocket BE) | 10, 11 | 20 | 21, 22 |
| 20 (WebSocket FE) | 17, 18, 19 | None | None |
| 21 (PM2 Service) | 6, 11 | 22, 28, 30 | 19 |
| 22 (Git Deploy) | 11, 21 | 30 | 19, 23, 25 |
| 23 (Env Encryption) | 8 | 22 | 24, 25 |
| 24 (Teams/RBAC) | 7, 9 | None | 22, 23 |
| 25 (Webhooks) | 10 | 30 | 22, 23, 24 |
| 26 (Celery Jobs) | 5, 11 | 22, 28 | 27, 29 |
| 27 (SSL) | 6 | None | 28, 29 |
| 28 (Monitoring) | 6, 26 | None | 27, 29 |
| 29 (Email) | 11 | None | 27, 28 |
| 30 (Health Checks) | 21, 22, 25 | 34 | 31, 32, 33 |
| 31 (Backups) | 4 | None | 30, 32, 33 |
| 32 (CLI) | 11 | None | 30, 31, 33 |
| 33 (Cost Display) | 11 | None | 30, 31, 32 |
| 34 (E2E Tests) | 30 | None | 35, 36 |
| 35 (Performance) | 34 | None | 36 |
| 36 (Docs) | 35 | None | None |

### Agent Dispatch Summary

| Wave | Tasks | Recommended Approach |
|------|-------|---------------------|
| 1 | 1-6 | Parallel dispatch - all independent setup tasks |
| 2 | 7-12 | Semi-parallel - groups (7-8), (9-10) can parallel, then 11-12 |
| 3 | 13-18 | Semi-parallel - groups (13-14), (15), (16) then (17-18) |
| 4 | 19-26 | Semi-parallel - (19-21) parallel, then (22-26) parallel groups |
| 5 | 27-36 | Semi-parallel - (27-29), (30-33), (34-36) sequential groups |

---

## TODOs

### WAVE 1: Foundation Setup

- [ ] **1. Project Structure & Monorepo Setup**

  **What to do**:
  - Create root directory structure: `backend/`, `frontend/`, `cli/`, `scripts/`, `docs/`
  - Initialize root `package.json` with workspace configuration
  - Create `docker-compose.yml` for PostgreSQL and Redis
  - Set up shared configuration files (`.gitignore`, `.editorconfig`)
  - Create `README.md` with project overview and setup instructions

  **Must NOT do**:
  - Do not initialize git repos in subdirectories (single root repo)
  - Do not commit `.env` files or secrets
  - Do not use Docker for the application deployment (only for dev dependencies)

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: None required
  - **Rationale**: Simple directory creation and file scaffolding

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1
  - **Blocks**: Tasks 2, 3, 4, 5, 6
  - **Blocked By**: None (can start immediately)

  **Acceptance Criteria**:
  - [ ] Directory structure exists: `ls backend/ frontend/ cli/ scripts/ docs/` → all exist
  - [ ] Root package.json has workspaces: `cat package.json | grep -A 5 '"workspaces"'` → shows backend and frontend
  - [ ] Docker Compose exists: `test -f docker-compose.yml` → exit 0
  - [ ] README exists and is not empty: `test -s README.md` → exit 0

  **Commit**: YES
  - Message: `chore: initial monorepo structure setup`
  - Files: All created structure files

---

- [ ] **2. Backend Dependencies & FastAPI Setup**

  **What to do**:
  - Create Python virtual environment in `backend/`
  - Install FastAPI, Uvicorn, SQLAlchemy 2.0, Alembic, Celery, Redis, Pydantic
  - Create `backend/requirements.txt` with pinned versions
  - Set up FastAPI app structure: `main.py`, `config.py`, `api/` folder
  - Create basic "Hello World" endpoint to verify setup
  - Create `backend/.env.example` with all required environment variables

  **Must NOT do**:
  - Do not install sync SQLAlchemy (must use 2.0 async)
  - Do not use Flask or Django (must use FastAPI)
  - Do not skip version pinning in requirements.txt

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high` (Python backend expertise)
  - **Skills**: None specifically needed
  - **Rationale**: Requires Python ecosystem knowledge

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Task 1 complete)
  - **Parallel Group**: Wave 1
  - **Blocks**: Tasks 7, 8, 9, 10, 11, 12
  - **Blocked By**: Task 1

  **Acceptance Criteria**:
  - [ ] Virtual environment exists: `ls backend/venv` or `ls backend/.venv` → exists
  - [ ] FastAPI runs: `cd backend && source venv/bin/activate && python -c "import fastapi; print(fastapi.__version__)"` → version printed
  - [ ] Hello endpoint works: `cd backend && uvicorn main:app --host 0.0.0.0 --port 8000 &` then `curl http://localhost:8000/` → returns {"message":"Hello World"}
  - [ ] requirements.txt has >20 dependencies: `wc -l backend/requirements.txt` → >20 lines

  **Commit**: YES
  - Message: `feat(backend): setup FastAPI with core dependencies`
  - Files: `backend/requirements.txt`, `backend/main.py`, `backend/config.py`, `backend/.env.example`

---

- [ ] **3. Frontend Dependencies & Next.js Setup**

  **What to do**:
  - Initialize Next.js 14+ project in `frontend/` with TypeScript
  - Install Tailwind CSS and configure
  - Install shadcn/ui CLI and initialize
  - Install Framer Motion for animations
  - Install Zustand for state management
  - Install React Query (TanStack Query) for server state
  - Install WebSocket client library
  - Create basic page structure to verify setup

  **Must NOT do**:
  - Do not use Next.js < 14 (must have App Router)
  - Do not skip TypeScript configuration
  - Do not use Redux (use Zustand instead)
  - Do not use page router

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high` (Next.js expertise)
  - **Skills**: None specifically needed
  - **Rationale**: Requires Next.js 14+ and TypeScript knowledge

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Task 1 complete)
  - **Parallel Group**: Wave 1
  - **Blocks**: Tasks 13, 14, 15, 16, 17, 18
  - **Blocked By**: Task 1

  **Acceptance Criteria**:
  - [ ] Next.js runs: `cd frontend && bun dev &` then `curl http://localhost:3000` → returns HTML with Next.js
  - [ ] Tailwind configured: `grep -r "tailwindcss" frontend/package.json` → found
  - [ ] TypeScript strict mode: `grep '"strict": true' frontend/tsconfig.json` → found
  - [ ] shadcn/ui initialized: `ls frontend/components/ui` → directory exists

  **Commit**: YES
  - Message: `feat(frontend): setup Next.js 14 with Tailwind and shadcn/ui`
  - Files: `frontend/package.json`, `frontend/tsconfig.json`, `frontend/tailwind.config.ts`, `frontend/app/`

---

- [ ] **4. Database Setup (PostgreSQL)**

  **What to do**:
  - Configure PostgreSQL in `docker-compose.yml`
  - Create initial database and user
  - Test connection from backend
  - Create `backend/database.py` with async SQLAlchemy 2.0 setup
  - Create database URL configuration
  - Add PostgreSQL driver (asyncpg) to requirements

  **Must NOT do**:
  - Do not use SQLite for development (must use PostgreSQL)
  - Do not use sync SQLAlchemy engine
  - Do not skip connection pooling configuration

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: None required
  - **Rationale**: Docker-based setup, standard configuration

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Task 1 complete)
  - **Parallel Group**: Wave 1
  - **Blocks**: Tasks 7, 8, 31
  - **Blocked By**: Task 1

  **Acceptance Criteria**:
  - [ ] PostgreSQL container runs: `docker compose up -d postgres` → container starts
  - [ ] Database connection works: `cd backend && python -c "from database import engine; print('OK')"` → prints OK
  - [ ] asyncpg installed: `grep asyncpg backend/requirements.txt` → found
  - [ ] Database URL configured: `grep DATABASE_URL backend/.env.example` → found

  **Commit**: YES
  - Message: `feat(backend): setup PostgreSQL with async SQLAlchemy`
  - Files: `docker-compose.yml`, `backend/database.py`, `backend/requirements.txt`

---

- [ ] **5. Redis & Celery Setup**

  **What to do**:
  - Configure Redis in `docker-compose.yml`
  - Install Celery and Redis client in backend
  - Create `backend/celery_app.py` with Celery configuration
  - Create example task to verify setup
  - Configure Celery to use Redis as broker and backend
  - Create `backend/tasks/` directory for job definitions

  **Must NOT do**:
  - Do not use RabbitMQ (must use Redis)
  - Do not skip task result backend configuration
  - Do not use sync Celery tasks (use async where possible)

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: None required
  - **Rationale**: Standard Celery + Redis configuration

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Task 1 complete)
  - **Parallel Group**: Wave 1
  - **Blocks**: Tasks 26
  - **Blocked By**: Task 1

  **Acceptance Criteria**:
  - [ ] Redis container runs: `docker compose up -d redis` → container starts
  - [ ] Celery starts: `cd backend && celery -A celery_app worker --loglevel=info &` → worker starts
  - [ ] Task execution works: `cd backend && python -c "from tasks.example import add; print(add.delay(2,3).get())"` → prints 5
  - [ ] Redis client installed: `grep redis backend/requirements.txt` → found

  **Commit**: YES
  - Message: `feat(backend): setup Celery with Redis broker`
  - Files: `docker-compose.yml`, `backend/celery_app.py`, `backend/tasks/__init__.py`

---

- [ ] **6. Traefik & PM2 Setup**

  **What to do**:
  - Configure Traefik in `docker-compose.yml` for reverse proxy
  - Create Traefik dynamic configuration directory
  - Install PM2 globally: `npm install -g pm2`
  - Create `ecosystem.config.js` for PM2 process management
  - Configure PM2 for log rotation
  - Test PM2 process creation with simple app
  - Create Let's Encrypt certificate resolver config

  **Must NOT do**:
  - Do not use Nginx instead of Traefik (must use Traefik for dynamic config)
  - Do not skip SSL certificate configuration
  - Do not use Docker for app deployments (PM2 only)

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high` (DevOps/infrastructure)
  - **Skills**: None specifically needed
  - **Rationale**: Requires infrastructure and PM2 knowledge

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Task 1 complete)
  - **Parallel Group**: Wave 1
  - **Blocks**: Tasks 21, 27, 28
  - **Blocked By**: Task 1

  **Acceptance Criteria**:
  - [ ] Traefik container runs: `docker compose up -d traefik` → container starts
  - [ ] PM2 installed: `pm2 --version` → version printed
  - [ ] PM2 process works: `echo 'console.log("test")' > /tmp/test.js && pm2 start /tmp/test.js --name test && pm2 list` → shows "test" process
  - [ ] Let's Encrypt config exists: `test -f traefik/traefik.yml` → exit 0

  **Commit**: YES
  - Message: `feat(infra): setup Traefik reverse proxy and PM2`
  - Files: `docker-compose.yml`, `ecosystem.config.js`, `traefik/`

---

### WAVE 2: Backend Core

- [ ] **7. SQLAlchemy Models & Alembic**

  **What to do**:
  - Create all SQLAlchemy 2.0 models based on schema design:
    - `tenants`, `users`, `projects`, `services`, `deployments`, `builds`
    - `environment_variables`, `teams`, `team_members`, `webhooks`
  - Configure Alembic for migrations
  - Create initial migration
  - Apply migration to database
  - Add model relationships and indexes

  **Must NOT do**:
  - Do not use SQLAlchemy 1.x style (must use 2.0 declarative)
  - Do not skip foreign key constraints
  - Do not skip index creation on frequently queried columns

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high` (Database/SQLAlchemy)
  - **Skills**: None specifically needed
  - **Rationale**: Requires SQLAlchemy 2.0 and database design expertise

  **Parallelization**:
  - **Can Run In Parallel**: NO (must be sequential)
  - **Blocks**: Tasks 8, 11, 24
  - **Blocked By**: Tasks 2, 4

  **Acceptance Criteria**:
  - [ ] All models created: `ls backend/models/*.py | wc -l` → >= 10 files
  - [ ] Alembic initialized: `ls backend/alembic` → directory exists
  - [ ] Migration created: `ls backend/alembic/versions/*.py | wc -l` → >= 1 file
  - [ ] Tables exist in DB: `docker compose exec postgres psql -U paas -c "\dt"` → shows all tables

  **Commit**: YES
  - Message: `feat(backend): create SQLAlchemy models and initial migration`
  - Files: `backend/models/`, `backend/alembic/`

---

- [ ] **8. Repository Pattern Implementation**

  **What to do**:
  - Create repository classes for each entity
  - Implement CRUD operations with async/await
  - Add pagination support
  - Add filtering and sorting
  - Create `backend/repositories/` directory
  - Add unit tests for repositories

  **Must NOT do**:
  - Do not put database logic directly in endpoints
  - Do not use sync database operations
  - Do not skip error handling in repositories

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high` (Python architecture)
  - **Skills**: None specifically needed
  - **Rationale**: Requires clean architecture and repository pattern knowledge

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Blocks**: Tasks 11, 23
  - **Blocked By**: Task 7

  **Acceptance Criteria**:
  - [ ] Repository classes exist: `ls backend/repositories/*.py | wc -l` → >= 5 files
  - [ ] Repository methods are async: `grep "async def" backend/repositories/*.py | wc -l` → >10 methods
  - [ ] CRUD operations work: `cd backend && pytest tests/repositories/ -v` → all tests pass

  **Commit**: YES
  - Message: `feat(backend): implement repository pattern for data access`
  - Files: `backend/repositories/`

---

- [ ] **9. GitHub OAuth Authentication**

  **What to do**:
  - Register OAuth app on GitHub
  - Create OAuth flow endpoints: `/auth/github/login`, `/auth/github/callback`
  - Implement GitHub API user fetching
  - Create user record in database after OAuth
  - Store GitHub access token (encrypted)
  - Handle OAuth errors and edge cases

  **Must NOT do**:
  - Do not store plain text GitHub tokens
  - Do not skip state parameter validation (CSRF protection)
  - Do not allow multiple OAuth providers for MVP

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high` (Authentication/security)
  - **Skills**: None specifically needed
  - **Rationale**: Requires OAuth 2.0 flow implementation

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Blocks**: Tasks 10, 15, 24
  - **Blocked By**: Task 2

  **Acceptance Criteria**:
  - [ ] OAuth endpoints exist: `grep -r "github" backend/api/auth*.py` → found
  - [ ] GitHub token encrypted: `grep "encrypt" backend/services/auth.py` → found
  - [ ] User creation works: Manual test via browser OAuth flow

  **Commit**: YES
  - Message: `feat(backend): implement GitHub OAuth authentication`
  - Files: `backend/api/auth.py`, `backend/services/auth.py`

---

- [ ] **10. JWT Token Management**

  **What to do**:
  - Implement JWT access token generation
  - Implement JWT refresh token generation
  - Create token refresh endpoint
  - Add JWT validation middleware
  - Configure token expiration times (access: 15min, refresh: 7days)
  - Implement HTTP-only cookie handling
  - Add token blacklisting for logout

  **Must NOT do**:
  - Do not store tokens in localStorage (must use HTTP-only cookies)
  - Do not skip refresh token rotation
  - Do not use weak JWT secrets

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high` (Security/JWT)
  - **Skills**: None specifically needed
  - **Rationale**: Requires JWT best practices and security knowledge

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Blocks**: Tasks 11, 15, 19, 25
  - **Blocked By**: Task 9

  **Acceptance Criteria**:
  - [ ] JWT library installed: `grep "pyjwt\|jose" backend/requirements.txt` → found
  - [ ] Token endpoints exist: `grep -r "refresh" backend/api/auth*.py` → found
  - [ ] Middleware validates tokens: `grep "JWT" backend/middleware/*.py` → found
  - [ ] HTTP-only cookies: `grep "httponly" backend/api/auth*.py` → found (case insensitive)

  **Commit**: YES
  - Message: `feat(backend): implement JWT token management`
  - Files: `backend/services/jwt.py`, `backend/middleware/auth.py`

---

- [ ] **11. Core API Endpoints (Projects, Services)**

  **What to do**:
  - Create CRUD endpoints for projects: `GET/POST/PUT/DELETE /api/v1/projects`
  - Create CRUD endpoints for services: `GET/POST/PUT/DELETE /api/v1/services`
  - Create service action endpoints: `POST /api/v1/services/{id}/deploy`
  - Create deployment list endpoint: `GET /api/v1/services/{id}/deployments`
  - Add pagination, filtering, sorting
  - Add comprehensive request/response validation with Pydantic

  **Must NOT do**:
  - Do not skip input validation
  - Do not return raw database models (use Pydantic schemas)
  - Do not skip authorization checks

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high` (API design)
  - **Skills**: None specifically needed
  - **Rationale**: Requires RESTful API design and FastAPI expertise

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Blocks**: Tasks 19, 21, 22, 26, 29, 32, 33
  - **Blocked By**: Tasks 7, 8, 10

  **Acceptance Criteria**:
  - [ ] Project endpoints work: `curl -s http://localhost:8000/api/v1/projects | jq '. | length'` → returns array
  - [ ] Service endpoints work: `curl -s http://localhost:8000/api/v1/services | jq '. | length'` → returns array
  - [ ] Deploy endpoint exists: `grep "deploy" backend/api/services.py` → found
  - [ ] Pydantic schemas exist: `ls backend/schemas/*.py | wc -l` → >= 5 files

  **Commit**: YES
  - Message: `feat(backend): implement core project and service API endpoints`
  - Files: `backend/api/projects.py`, `backend/api/services.py`, `backend/schemas/`

---

- [ ] **12. Error Handling & Pydantic Validation**

  **What to do**:
  - Create global exception handler middleware
  - Define custom exception classes
  - Implement structured error responses
  - Add request validation with Pydantic v2
  - Add field-level error messages
  - Create error logging service
  - Add validation for all API inputs

  **Must NOT do**:
  - Do not expose internal error details to clients
  - Do not skip logging of errors
  - Do not use Pydantic v1 (must use v2)

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: None required
  - **Rationale**: Standard FastAPI error handling patterns

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Task 11)
  - **Blocks**: None
  - **Blocked By**: Task 2

  **Acceptance Criteria**:
  - [ ] Exception handlers exist: `grep "ExceptionHandler" backend/middleware/*.py` → found
  - [ ] Validation errors return 422: `curl -s -w "%{http_code}" -X POST http://localhost:8000/api/v1/projects -d '{}' | tail -1` → 422
  - [ ] Structured errors: `curl -s http://localhost:8000/api/v1/invalid | jq 'has("detail")'` → true

  **Commit**: YES
  - Message: `feat(backend): implement comprehensive error handling and validation`
  - Files: `backend/middleware/error_handler.py`, `backend/exceptions/`

---

### WAVE 3: Frontend Core

- [ ] **13. Tailwind Config & Design System**

  **What to do**:
  - Configure custom color palette (slate-950, indigo-600, violet-600, cyan-400)
  - Add custom fonts (Inter/Geist, JetBrains Mono)
  - Create glassmorphism utility classes
  - Configure Tailwind plugins
  - Create global CSS with dark mode default
  - Add custom animations keyframes

  **Must NOT do**:
  - Do not use default Tailwind colors (must match Railway aesthetic)
  - Do not skip dark mode configuration
  - Do not use light mode as default

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high` (UI/Design)
  - **Skills**: None specifically needed
  - **Rationale**: Requires Tailwind CSS and design system knowledge

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Blocks**: Tasks 14, 16
  - **Blocked By**: Task 3

  **Acceptance Criteria**:
  - [ ] Custom colors in config: `grep "slate-950" frontend/tailwind.config.ts` → found
  - [ ] Glassmorphism utilities: `grep "backdrop-blur" frontend/tailwind.config.ts` → found
  - [ ] Dark mode default: `grep "darkMode" frontend/tailwind.config.ts` → found
  - [ ] Custom fonts: `grep "JetBrains Mono\|Inter" frontend/tailwind.config.ts` → found

  **Commit**: YES
  - Message: `feat(frontend): configure Tailwind with Railway design system`
  - Files: `frontend/tailwind.config.ts`, `frontend/app/globals.css`

---

- [ ] **14. shadcn/ui Components Setup**

  **What to do**:
  - Initialize shadcn/ui in frontend
  - Install base components: Button, Card, Input, Dialog, Dropdown
  - Install data display components: Table, Badge, Tabs
  - Install feedback components: Toast, Alert
  - Customize component styles for dark theme
  - Create component barrel exports

  **Must NOT do**:
  - Do not use default shadcn light theme
  - Do not skip component customization
  - Do not install unnecessary components

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: None required
  - **Rationale**: Standard shadcn/ui installation

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Blocks**: Tasks 16, 17, 18
  - **Blocked By**: Task 13

  **Acceptance Criteria**:
  - [ ] shadcn components exist: `ls frontend/components/ui/*.tsx | wc -l` → >= 10 files
  - [ ] Components customized: `grep "slate-950\|gray-900" frontend/components/ui/button.tsx` → found
  - [ ] Toast system working: `grep "Toaster" frontend/app/layout.tsx` → found

  **Commit**: YES
  - Message: `feat(frontend): setup shadcn/ui components with dark theme`
  - Files: `frontend/components/ui/`, `frontend/components.json`

---

- [ ] **15. Authentication UI (Login, Callback)**

  **What to do**:
  - Create `/login` page with GitHub OAuth button
  - Create `/auth/callback` page for OAuth callback handling
  - Implement JWT token storage (HTTP-only cookies)
  - Add loading states and error handling
  - Create auth context/provider
  - Add logout functionality

  **Must NOT do**:
  - Do not store JWT in localStorage
  - Do not skip error handling for OAuth failures
  - Do not allow unauthenticated access to protected routes

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high` (React/Auth)
  - **Skills**: None specifically needed
  - **Rationale**: Requires React state management and OAuth flow

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Blocks**: Task 16
  - **Blocked By**: Tasks 3, 10

  **Acceptance Criteria**:
  - [ ] Login page exists: `test -f frontend/app/login/page.tsx` → exit 0
  - [ ] Callback page exists: `test -f frontend/app/auth/callback/page.tsx` → exit 0
  - [ ] Auth context exists: `test -f frontend/lib/auth.tsx` → exit 0
  - [ ] GitHub button styled: `grep -r "Sign in with GitHub\|Continue with GitHub" frontend/app/login` → found

  **Commit**: YES
  - Message: `feat(frontend): implement GitHub OAuth login UI`
  - Files: `frontend/app/login/`, `frontend/app/auth/callback/`, `frontend/lib/auth.tsx`

---

- [ ] **16. Dashboard Layout & Navigation**

  **What to do**:
  - Create dashboard layout with sidebar navigation
  - Implement top navigation bar with user menu
  - Add project selector dropdown
  - Create responsive layout (mobile sidebar)
  - Add breadcrumb navigation
  - Implement navigation guards (protected routes)

  **Must NOT do**:
  - Do not skip mobile responsiveness
  - Do not hardcode navigation items
  - Do not skip active state styling

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high` (UI/UX)
  - **Skills**: None specifically needed
  - **Rationale**: Requires complex layout and navigation patterns

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Blocks**: Tasks 17, 18, 20
  - **Blocked By**: Tasks 13, 14, 15

  **Acceptance Criteria**:
  - [ ] Dashboard layout exists: `test -f frontend/app/dashboard/layout.tsx` → exit 0
  - [ ] Sidebar navigation: `grep -r "Sidebar\|Navigation" frontend/app/dashboard/layout.tsx` → found
  - [ ] Protected route: `grep -r "useAuth\|ProtectedRoute" frontend/middleware.ts` → found
  - [ ] User menu: `grep -r "UserButton\|Avatar" frontend/components/` → found

  **Commit**: YES
  - Message: `feat(frontend): create dashboard layout and navigation`
  - Files: `frontend/app/dashboard/`, `frontend/components/sidebar.tsx`, `frontend/middleware.ts`

---

- [ ] **17. Project Management UI**

  **What to do**:
  - Create `/dashboard` page showing project list
  - Create project creation modal
  - Create `/projects/[id]` page with project details
  - Add project settings panel
  - Implement project delete with confirmation
  - Add empty state for new users

  **Must NOT do**:
  - Do not skip empty states
  - Do not allow deletion without confirmation
  - Do not skip loading skeletons

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high` (React/CRUD)
  - **Skills**: None specifically needed
  - **Rationale**: Requires CRUD UI implementation

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Task 18)
  - **Blocks**: Task 20
  - **Blocked By**: Task 16

  **Acceptance Criteria**:
  - [ ] Project list page: `test -f frontend/app/dashboard/page.tsx` → exit 0
  - [ ] Project detail page: `test -f frontend/app/projects/[id]/page.tsx` → exit 0
  - [ ] Create modal: `grep -r "Dialog\|Modal" frontend/app/dashboard/` → found
  - [ ] API integration: `grep -r "useQuery\|fetch" frontend/app/dashboard/page.tsx` → found

  **Commit**: YES
  - Message: `feat(frontend): implement project management UI`
  - Files: `frontend/app/dashboard/page.tsx`, `frontend/app/projects/[id]/page.tsx`

---

- [ ] **18. Service Management UI**

  **What to do**:
  - Create service list view in project page
  - Create service creation modal
  - Create `/services/[id]` page with service details
  - Add service control buttons (start/stop/restart/deploy)
  - Show service status with color indicators
  - Add service configuration panel

  **Must NOT do**:
  - Do not skip real-time status updates
  - Do not allow destructive actions without confirmation
  - Do not skip deployment trigger UI

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high` (React/State Management)
  - **Skills**: None specifically needed
  - **Rationale**: Requires complex state management for service controls

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Task 17)
  - **Blocks**: Task 20
  - **Blocked By**: Task 16

  **Acceptance Criteria**:
  - [ ] Service detail page: `test -f frontend/app/services/[id]/page.tsx` → exit 0
  - [ ] Control buttons: `grep -r "Start\|Stop\|Restart\|Deploy" frontend/app/services/[id]/` → found
  - [ ] Status indicators: `grep -r "online\|stopped\|error\|running" frontend/components/` → found
  - [ ] GitHub repo selector: `grep -r "github\|repository" frontend/app/services/` → found

  **Commit**: YES
  - Message: `feat(frontend): implement service management UI`
  - Files: `frontend/app/services/[id]/page.tsx`, `frontend/components/service-controls.tsx`

---

### WAVE 4: Advanced Features

- [ ] **19. WebSocket Log Streaming (Backend)**

  **What to do**:
  - Implement WebSocket ConnectionManager with heartbeat
  - Create `/ws/logs/{service_id}` WebSocket endpoint
  - Stream PM2 process logs to connected clients
  - Implement Redis pub/sub for multi-instance scaling
  - Add authentication for WebSocket connections
  - Handle connection cleanup on disconnect
  - Implement log buffering for replay

  **Must NOT do**:
  - Do not skip authentication on WebSocket connections
  - Do not skip connection cleanup
  - Do not broadcast logs to unauthorized clients

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high` (WebSocket/Real-time)
  - **Skills**: None specifically needed
  - **Rationale**: Requires WebSocket protocol and real-time systems knowledge

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 21, 22)
  - **Blocks**: Task 20
  - **Blocked By**: Tasks 10, 11

  **Acceptance Criteria**:
  - [ ] WebSocket endpoint exists: `grep -r "websocket\|WebSocket" backend/api/` → found
  - [ ] ConnectionManager exists: `test -f backend/services/websocket.py` → exit 0
  - [ ] PM2 log streaming: `grep -r "pm2.*log\|logs" backend/services/websocket.py` → found
  - [ ] Redis pub/sub: `grep -r "pubsub\|publish\|subscribe" backend/services/websocket.py` → found

  **Commit**: YES
  - Message: `feat(backend): implement WebSocket log streaming`
  - Files: `backend/api/websocket.py`, `backend/services/websocket.py`

---

- [ ] **20. WebSocket Client (Frontend)**

  **What to do**:
  - Create log viewer component with WebSocket client
  - Implement auto-reconnect logic
  - Add connection status indicator
  - Implement log filtering and search
  - Add ANSI color code rendering
  - Create scroll-to-bottom button
  - Implement log export/download

  **Must NOT do**:
  - Do not skip reconnection handling
  - Do not buffer all logs in memory (use virtual scrolling)
  - Do not skip connection error handling

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high` (React/WebSocket)
  - **Skills**: None specifically needed
  - **Rationale**: Requires WebSocket client implementation and performance optimization

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Blocks**: None
  - **Blocked By**: Tasks 17, 18, 19

  **Acceptance Criteria**:
  - [ ] Log viewer component: `test -f frontend/components/log-viewer.tsx` → exit 0
  - [ ] WebSocket hook: `test -f frontend/hooks/use-websocket.ts` → exit 0
  - [ ] ANSI rendering: `grep -r "ansi\|ANS" frontend/components/log-viewer.tsx` → found
  - [ ] Auto-reconnect: `grep -r "reconnect\|onClose" frontend/hooks/use-websocket.ts` → found

  **Commit**: YES
  - Message: `feat(frontend): implement WebSocket log viewer with ANSI support`
  - Files: `frontend/components/log-viewer.tsx`, `frontend/hooks/use-websocket.ts`

---

- [ ] **21. PM2 Process Management Service**

  **What to do**:
  - Create PM2 service wrapper class
  - Implement start/stop/restart/delete methods
  - Add process status monitoring
  - Implement graceful shutdown handling
  - Add log file path management
  - Create health check integration
  - Handle PM2 connection lifecycle

  **Must NOT do**:
  - Do not skip graceful shutdown
  - Do not leave PM2 connections open
  - Do not skip error handling for PM2 failures

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high` (Process Management)
  - **Skills**: None specifically needed
  - **Rationale**: Requires PM2 programmatic API expertise

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 19, 22)
  - **Blocks**: Tasks 22, 28, 30
  - **Blocked By**: Tasks 6, 11

  **Acceptance Criteria**:
  - [ ] PM2 service exists: `test -f backend/services/pm2.py` → exit 0
  - [ ] Process methods: `grep -r "start\|stop\|restart\|delete" backend/services/pm2.py | wc -l` → >= 4
  - [ ] Status monitoring: `grep -r "describe\|list\|status" backend/services/pm2.py` → found
  - [ ] Graceful shutdown: `grep -r "graceful\|SIGTERM" backend/services/pm2.py` → found

  **Commit**: YES
  - Message: `feat(backend): implement PM2 process management service`
  - Files: `backend/services/pm2.py`

---

- [ ] **22. Git-based Deployment Pipeline**

  **What to do**:
  - Implement Git repository cloning
  - Detect build commands from package.json/runtime
  - Execute build process with log streaming
  - Update PM2 process with new deployment
  - Handle rollback on failure
  - Store deployment history
  - Update service status throughout deployment

  **Must NOT do**:
  - Do not skip build failure handling
  - Do not deploy without successful build
  - Do not skip deployment history tracking

  **Recommended Agent Profile**:
  - **Category**: `ultrabrain` (Complex system integration)
  - **Skills**: None specifically needed
  - **Rationale**: Requires complex orchestration of Git, builds, and process management

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 19, 23, 24, 25)
  - **Blocks**: Task 30
  - **Blocked By**: Tasks 11, 21

  **Acceptance Criteria**:
  - [ ] Deployment service: `test -f backend/services/deployment.py` → exit 0
  - [ ] Git cloning: `grep -r "git clone\|subprocess.*git" backend/services/deployment.py` → found
  - [ ] Build execution: `grep -r "npm install\|pip install\|build" backend/services/deployment.py` → found
  - [ ] Rollback handling: `grep -r "rollback\|restore" backend/services/deployment.py` → found

  **Commit**: YES
  - Message: `feat(backend): implement git-based deployment pipeline`
  - Files: `backend/services/deployment.py`

---

- [ ] **23. Environment Variable Encryption**

  **What to do**:
  - Implement AES-256-GCM encryption service
  - Create environment variable CRUD endpoints
  - Integrate with PM2 process startup
  - Add secret vs non-secret flag
  - Implement key rotation support
  - Create environment variable UI

  **Must NOT do**:
  - Do not use Fernet (use AES-256-GCM)
  - Do not store plain text secrets in database
  - Do not skip encryption key management

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high` (Cryptography)
  - **Skills**: None specifically needed
  - **Rationale**: Requires encryption best practices

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 22, 24, 25)
  - **Blocks**: None
  - **Blocked By**: Task 8

  **Acceptance Criteria**:
  - [ ] Encryption service: `test -f backend/services/encryption.py` → exit 0
  - [ ] AES-256-GCM: `grep -r "AES\|GCM" backend/services/encryption.py` → found
  - [ ] Env var endpoints: `grep -r "environment" backend/api/*.py` → found
  - [ ] PM2 integration: `grep -r "env\|environment" backend/services/pm2.py` → found

  **Commit**: YES
  - Message: `feat(backend): implement AES-256-GCM environment variable encryption`
  - Files: `backend/services/encryption.py`, `backend/api/environment.py`

---

- [ ] **24. Team Workspaces & RBAC**

  **What to do**:
  - Implement team creation and management
  - Create member invitation system
  - Implement role-based access control (owner, admin, member)
  - Add permission checks to all endpoints
  - Create team member management UI
  - Implement team switching
  - Add audit logging for team actions

  **Must NOT do**:
  - Do not skip permission checks on any endpoint
  - Do not allow privilege escalation
  - Do not skip invitation token expiration

  **Recommended Agent Profile**:
  - **Category**: `ultrabrain` (Authorization/RBAC)
  - **Skills**: None specifically needed
  - **Rationale**: Requires complex RBAC implementation

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 22, 23, 25)
  - **Blocks**: None
  - **Blocked By**: Tasks 7, 9

  **Acceptance Criteria**:
  - [ ] Team endpoints: `test -f backend/api/teams.py` → exit 0
  - [ ] RBAC middleware: `test -f backend/middleware/rbac.py` → exit 0
  - [ ] Roles defined: `grep -r "owner\|admin\|member" backend/models/*.py` → found
  - [ ] Invitation system: `grep -r "invite\|invitation" backend/api/teams.py` → found

  **Commit**: YES
  - Message: `feat(backend): implement team workspaces and RBAC`
  - Files: `backend/api/teams.py`, `backend/middleware/rbac.py`

---

- [ ] **25. Webhook Handlers**

  **What to do**:
  - Create GitHub webhook handler endpoint
  - Implement HMAC signature verification
  - Parse push events and trigger deployments
  - Handle ping events for webhook setup
  - Add webhook configuration UI
  - Implement webhook secret management
  - Add webhook delivery logging

  **Must NOT do**:
  - Do not skip HMAC signature verification
  - Do not deploy without verifying signature
  - Do not skip webhook error handling

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high` (Webhooks/Security)
  - **Skills**: None specifically needed
  - **Rationale**: Requires webhook security and event handling

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 22, 23, 24)
  - **Blocks**: Task 30
  - **Blocked By**: Task 10

  **Acceptance Criteria**:
  - [ ] Webhook endpoint: `test -f backend/api/webhooks.py` → exit 0
  - [ ] HMAC verification: `grep -r "hmac\|signature" backend/api/webhooks.py` → found
  - [ ] GitHub events: `grep -r "push\|ping\|github" backend/api/webhooks.py` → found
  - [ ] Deployment trigger: `grep -r "deploy\|trigger" backend/api/webhooks.py` → found

  **Commit**: YES
  - Message: `feat(backend): implement GitHub webhook handlers with HMAC verification`
  - Files: `backend/api/webhooks.py`

---

- [ ] **26. Background Jobs (Celery)**

  **What to do**:
  - Create Celery tasks: build_service, deploy_service, stop_service
  - Implement task retry policies
  - Add task monitoring dashboard API
  - Create task result storage
  - Implement task chaining for deployment pipeline
  - Add task timeout handling

  **Must NOT do**:
  - Do not skip task retry configuration
  - Do not skip timeout handling
  - Do not skip task result persistence

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high` (Celery/Distributed Systems)
  - **Skills**: None specifically needed
  - **Rationale**: Requires Celery task design patterns

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 22, 27)
  - **Blocks**: Task 28
  - **Blocked By**: Tasks 5, 11

  **Acceptance Criteria**:
  - [ ] Celery tasks exist: `ls backend/tasks/*.py | wc -l` → >= 5 files
  - [ ] Task decorators: `grep -r "@app.task" backend/tasks/*.py | wc -l` → >= 5
  - [ ] Retry config: `grep -r "retry\|max_retries" backend/tasks/*.py` → found
  - [ ] Task chaining: `grep -r "chain\|link" backend/tasks/*.py` → found

  **Commit**: YES
  - Message: `feat(backend): implement Celery background jobs for deployments`
  - Files: `backend/tasks/build.py`, `backend/tasks/deploy.py`, `backend/tasks/monitor.py`

---

### WAVE 5: Production & Polish

- [ ] **27. SSL Certificate Automation**

  **What to do**:
  - Configure Traefik Let's Encrypt resolver
  - Implement automatic certificate provisioning
  - Add certificate renewal handling
  - Create custom domain placeholder logic
  - Add certificate status monitoring
  - Handle certificate errors gracefully

  **Must NOT do**:
  - Do not skip certificate renewal
  - Do not use self-signed certificates in production
  - Do not skip error handling for cert failures

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high` (DevOps/SSL)
  - **Skills**: None specifically needed
  - **Rationale**: Requires Let's Encrypt and Traefik expertise

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 26, 28, 29)
  - **Blocks**: None
  - **Blocked By**: Task 6

  **Acceptance Criteria**:
  - [ ] Let's Encrypt config: `grep -r "letsencrypt\|certificates" traefik/traefik.yml` → found
  - [ ] ACME configuration: `grep -r "acme\|email" traefik/traefik.yml` → found
  - [ ] HTTP challenge: `grep -r "httpChallenge\|tlsChallenge" traefik/traefik.yml` → found

  **Commit**: YES
  - Message: `feat(infra): configure automatic SSL certificates with Let's Encrypt`
  - Files: `traefik/traefik.yml`, `traefik/dynamic/`

---

- [ ] **28. Resource Monitoring & Analytics**

  **What to do**:
  - Collect CPU and memory metrics from PM2
  - Store metrics in time-series format
  - Create analytics API endpoints
  - Build resource usage charts in frontend
  - Implement historical data aggregation
  - Add cost estimation calculations
  - Create alerts for resource thresholds

  **Must NOT do**:
  - Do not skip historical data retention
  - Do not collect metrics synchronously (use background tasks)
  - Do not skip cost estimation formula

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high` (Monitoring/Data)
  - **Skills**: None specifically needed
  - **Rationale**: Requires metrics collection and visualization

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 26, 27, 29)
  - **Blocks**: None
  - **Blocked By**: Tasks 6, 26

  **Acceptance Criteria**:
  - [ ] Metrics collection: `test -f backend/services/metrics.py` → exit 0
  - [ ] PM2 metrics: `grep -r "cpu\|memory\|monit" backend/services/metrics.py` → found
  - [ ] Analytics API: `grep -r "analytics\|metrics" backend/api/*.py` → found
  - [ ] Frontend charts: `grep -r "Recharts\|chart" frontend/components/` → found

  **Commit**: YES
  - Message: `feat: implement resource monitoring and analytics`
  - Files: `backend/services/metrics.py`, `backend/api/analytics.py`, `frontend/components/resource-charts.tsx`

---

- [ ] **29. Email Notifications (Resend)**

  **What to do**:
  - Integrate Resend API for email delivery
  - Create email templates for deployment events
  - Implement deployment failure notifications
  - Add team invitation emails
  - Create email preference settings
  - Add email delivery tracking

  **Must NOT do**:
  - Do not skip email template design
  - Do not send emails synchronously (use background tasks)
  - Do not skip bounce handling

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: None required
  - **Rationale**: Standard email API integration

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 26, 27, 28)
  - **Blocks**: None
  - **Blocked By**: Task 11

  **Acceptance Criteria**:
  - [ ] Resend integration: `grep -r "resend\|email" backend/services/email.py` → found
  - [ ] Email templates: `ls backend/templates/email/*.html | wc -l` → >= 2 files
  - [ ] Deployment notifications: `grep -r "deployment.*email\|notify" backend/tasks/deploy.py` → found

  **Commit**: YES
  - Message: `feat(backend): integrate Resend for email notifications`
  - Files: `backend/services/email.py`, `backend/templates/email/`

---

- [ ] **30. Health Checks & Auto-restart**

  **What to do**:
  - Implement service health check endpoints
  - Configure PM2 auto-restart policies
  - Add health status to service model
  - Create health check monitoring job
  - Implement failure notifications
  - Add graceful degradation handling
  - Create health dashboard in frontend

  **Must NOT do**:
  - Do not skip health check implementation
  - Do not use aggressive restart policies
  - Do not skip failure notification

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high` (Reliability)
  - **Skills**: None specifically needed
  - **Rationale**: Requires health check design and monitoring

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 31, 32, 33)
  - **Blocks**: Task 34
  - **Blocked By**: Tasks 21, 22, 25

  **Acceptance Criteria**:
  - [ ] Health check endpoint: `grep -r "health\|ping" backend/api/*.py` → found
  - [ ] PM2 auto-restart: `grep -r "max_restarts\|autorestart" backend/services/pm2.py` → found
  - [ ] Health status: `grep -r "health_status\|healthy" backend/models/*.py` → found
  - [ ] Monitoring job: `grep -r "health.*check\|monitor" backend/tasks/*.py` → found

  **Commit**: YES
  - Message: `feat: implement health checks and auto-restart policies`
  - Files: `backend/api/health.py`, `backend/tasks/health_monitor.py`

---

- [ ] **31. Database Backup System**

  **What to do**:
  - Implement automated database backups
  - Create backup file management
  - Add backup restoration capability
  - Implement backup scheduling
  - Add backup storage (local/S3 placeholder)
  - Create backup UI in frontend

  **Must NOT do**:
  - Do not store backups unencrypted
  - Do not skip backup verification
  - Do not skip retention policy

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high` (Database/DevOps)
  - **Skills**: None specifically needed
  - **Rationale**: Requires PostgreSQL backup procedures

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 30, 32, 33)
  - **Blocks**: None
  - **Blocked By**: Task 4

  **Acceptance Criteria**:
  - [ ] Backup service: `test -f backend/services/backup.py` → exit 0
  - [ ] pg_dump usage: `grep -r "pg_dump\|backup" backend/services/backup.py` → found
  - [ ] Scheduled backups: `grep -r "schedule\|cron\|celery" backend/tasks/backup.py` → found

  **Commit**: YES
  - Message: `feat(backend): implement database backup system`
  - Files: `backend/services/backup.py`, `backend/tasks/backup.py`

---

- [ ] **32. CLI Tool Implementation**

  **What to do**:
  - Create Python CLI package structure
  - Implement authentication command
  - Add project listing command
  - Create deployment commands (deploy, logs, status)
  - Add configuration file management
  - Implement local project scaffolding
  - Add interactive mode

  **Must NOT do**:
  - Do not skip configuration persistence
  - Do not skip error handling
  - Do not hardcode API URLs

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high` (CLI/Python)
  - **Skills**: None specifically needed
  - **Rationale**: Requires CLI framework knowledge (Click/Typer)

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 30, 31, 33)
  - **Blocks**: None
  - **Blocked By**: Task 11

  **Acceptance Criteria**:
  - [ ] CLI package: `test -f cli/pyproject.toml` → exit 0
  - [ ] CLI entry point: `test -f cli/railway_cli/__init__.py` → exit 0
  - [ ] Click/Typer: `grep -r "click\|typer" cli/pyproject.toml` → found
  - [ ] Deploy command: `grep -r "deploy\|logs\|status" cli/railway_cli/commands.py` → found

  **Commit**: YES
  - Message: `feat(cli): implement deployment management CLI tool`
  - Files: `cli/`

---

- [ ] **33. Cost Estimation Display**

  **What to do**:
  - Implement cost calculation formulas
  - Create cost tracking per service
  - Add cost dashboard in frontend
  - Implement historical cost charts
  - Add cost alerts/notifications
  - Create resource usage to cost mapping

  **Must NOT do**:
  - Do not skip cost calculation documentation
  - Do not make costs too complex for MVP
  - Do not skip cost transparency

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: None required
  - **Rationale**: Simple cost calculation and display

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 30, 31, 32)
  - **Blocks**: None
  - **Blocked By**: Task 11

  **Acceptance Criteria**:
  - [ ] Cost service: `test -f backend/services/cost.py` → exit 0
  - [ ] Cost API: `grep -r "cost\|pricing" backend/api/*.py` → found
  - [ ] Cost UI: `grep -r "cost\|pricing\|\$" frontend/app/dashboard/` → found

  **Commit**: YES
  - Message: `feat: implement cost estimation display`
  - Files: `backend/services/cost.py`, `frontend/components/cost-display.tsx`

---

- [ ] **34. E2E Testing Suite**

  **What to do**:
  - Setup Playwright for E2E testing
  - Create authentication flow tests
  - Implement project creation tests
  - Add deployment flow E2E test
  - Create team invitation tests
  - Add WebSocket log streaming test
  - Implement CI test runner

  **Must NOT do**:
  - Do not skip test isolation
  - Do not hardcode test data
  - Do not skip cleanup after tests

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high` (Testing)
  - **Skills**: None specifically needed
  - **Rationale**: Requires E2E testing patterns

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Blocks**: None
  - **Blocked By**: Task 30

  **Acceptance Criteria**:
  - [ ] Playwright config: `test -f frontend/playwright.config.ts` → exit 0
  - [ ] Test files: `ls frontend/e2e/*.spec.ts | wc -l` → >= 5 files
  - [ ] Auth tests: `grep -r "auth\|login" frontend/e2e/*.spec.ts` → found
  - [ ] Deploy tests: `grep -r "deploy\|project" frontend/e2e/*.spec.ts` → found

  **Commit**: YES
  - Message: `test: implement comprehensive E2E test suite`
  - Files: `frontend/playwright.config.ts`, `frontend/e2e/`

---

- [ ] **35. Performance Optimization**

  **What to do**:
  - Add database query optimization
  - Implement Redis caching for frequent queries
  - Add frontend bundle optimization
  - Implement lazy loading for heavy components
  - Add database connection pooling tuning
  - Optimize WebSocket message batching
  - Add CDN configuration placeholders

  **Must NOT do**:
  - Do not optimize prematurely without metrics
  - Do not skip load testing
  - Do not break functionality for performance

  **Recommended Agent Profile**:
  - **Category**: `ultrabrain` (Performance Engineering)
  - **Skills**: None specifically needed
  - **Rationale**: Requires performance profiling and optimization

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Task 36)
  - **Blocks**: None
  - **Blocked By**: Task 34

  **Acceptance Criteria**:
  - [ ] Redis caching: `grep -r "cache\|redis" backend/services/cache.py` → found
  - [ ] Connection pooling: `grep -r "pool_size\|max_overflow" backend/database.py` → found
  - [ ] Frontend lazy loading: `grep -r "lazy\|dynamic" frontend/app/` → found
  - [ ] Query optimization: `grep -r "joinedload\|selectinload" backend/repositories/*.py` → found

  **Commit**: YES
  - Message: `perf: implement performance optimizations`
  - Files: `backend/services/cache.py`, `frontend/next.config.js`

---

- [ ] **36. Documentation**

  **What to do**:
  - Write API documentation (OpenAPI/Swagger)
  - Create setup and installation guide
  - Write architecture documentation
  - Create contribution guidelines
  - Add deployment guide
  - Write CLI usage documentation
  - Create troubleshooting guide

  **Must NOT do**:
  - Do not skip code examples
  - Do not skip troubleshooting section
  - Do not use outdated documentation formats

  **Recommended Agent Profile**:
  - **Category**: `writing`
  - **Skills**: None required
  - **Rationale**: Documentation writing task

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Task 35)
  - **Blocks**: None
  - **Blocked By**: Task 35

  **Acceptance Criteria**:
  - [ ] API docs: `test -f docs/api.md` → exit 0
  - [ ] Setup guide: `test -f docs/setup.md` → exit 0
  - [ ] Architecture docs: `test -f docs/architecture.md` → exit 0
  - [ ] Swagger UI: `grep -r "swagger\|openapi" backend/main.py` → found

  **Commit**: YES
  - Message: `docs: add comprehensive documentation`
  - Files: `docs/`

---

## Commit Strategy

| After Task | Message | Files | Verification |
|------------|---------|-------|--------------|
| 1 | `chore: initial monorepo structure setup` | All structure files | Directory check |
| 2 | `feat(backend): setup FastAPI with core dependencies` | `backend/requirements.txt`, `main.py` | Server starts |
| 3 | `feat(frontend): setup Next.js 14 with Tailwind and shadcn/ui` | `frontend/package.json`, `tsconfig.json` | Dev server runs |
| 4 | `feat(backend): setup PostgreSQL with async SQLAlchemy` | `docker-compose.yml`, `database.py` | Connection works |
| 5 | `feat(backend): setup Celery with Redis broker` | `docker-compose.yml`, `celery_app.py` | Worker starts |
| 6 | `feat(infra): setup Traefik reverse proxy and PM2` | `docker-compose.yml`, `ecosystem.config.js` | PM2 works |
| 7 | `feat(backend): create SQLAlchemy models and initial migration` | `backend/models/`, `alembic/` | Tables exist |
| 8 | `feat(backend): implement repository pattern for data access` | `backend/repositories/` | Tests pass |
| 9 | `feat(backend): implement GitHub OAuth authentication` | `backend/api/auth.py` | OAuth flow works |
| 10 | `feat(backend): implement JWT token management` | `backend/services/jwt.py` | Tokens validate |
| 11 | `feat(backend): implement core project and service API endpoints` | `backend/api/projects.py`, `services.py` | API responds |
| 12 | `feat(backend): implement comprehensive error handling and validation` | `backend/middleware/error_handler.py` | Errors structured |
| 13 | `feat(frontend): configure Tailwind with Railway design system` | `tailwind.config.ts` | Colors match spec |
| 14 | `feat(frontend): setup shadcn/ui components with dark theme` | `frontend/components/ui/` | Components work |
| 15 | `feat(frontend): implement GitHub OAuth login UI` | `frontend/app/login/`, `auth/callback/` | Login flow works |
| 16 | `feat(frontend): create dashboard layout and navigation` | `frontend/app/dashboard/`, `components/sidebar.tsx` | Layout renders |
| 17 | `feat(frontend): implement project management UI` | `frontend/app/dashboard/page.tsx`, `projects/[id]/` | CRUD works |
| 18 | `feat(frontend): implement service management UI` | `frontend/app/services/[id]/page.tsx` | Controls work |
| 19 | `feat(backend): implement WebSocket log streaming` | `backend/api/websocket.py` | WS connects |
| 20 | `feat(frontend): implement WebSocket log viewer with ANSI support` | `frontend/components/log-viewer.tsx` | Logs stream |
| 21 | `feat(backend): implement PM2 process management service` | `backend/services/pm2.py` | PM2 controls work |
| 22 | `feat(backend): implement git-based deployment pipeline` | `backend/services/deployment.py` | Deployments work |
| 23 | `feat(backend): implement AES-256-GCM environment variable encryption` | `backend/services/encryption.py` | Encryption works |
| 24 | `feat(backend): implement team workspaces and RBAC` | `backend/api/teams.py`, `middleware/rbac.py` | RBAC enforced |
| 25 | `feat(backend): implement GitHub webhook handlers with HMAC verification` | `backend/api/webhooks.py` | Webhooks work |
| 26 | `feat(backend): implement Celery background jobs for deployments` | `backend/tasks/*.py` | Jobs execute |
| 27 | `feat(infra): configure automatic SSL certificates with Let's Encrypt` | `traefik/traefik.yml` | SSL works |
| 28 | `feat: implement resource monitoring and analytics` | `backend/services/metrics.py`, `frontend/components/resource-charts.tsx` | Metrics display |
| 29 | `feat(backend): integrate Resend for email notifications` | `backend/services/email.py` | Emails sent |
| 30 | `feat: implement health checks and auto-restart policies` | `backend/api/health.py` | Health checks work |
| 31 | `feat(backend): implement database backup system` | `backend/services/backup.py` | Backups work |
| 32 | `feat(cli): implement deployment management CLI tool` | `cli/` | CLI works |
| 33 | `feat: implement cost estimation display` | `backend/services/cost.py` | Costs display |
| 34 | `test: implement comprehensive E2E test suite` | `frontend/playwright.config.ts`, `e2e/` | Tests pass |
| 35 | `perf: implement performance optimizations` | `backend/services/cache.py` | Performance improved |
| 36 | `docs: add comprehensive documentation` | `docs/` | Docs complete |

---

## Success Criteria

### Final Verification Commands

```bash
# Full system health check
docker compose ps  # All containers running

# Backend API check
curl http://localhost:8000/health  # Returns {"status":"ok"}

# Frontend check
curl http://localhost:3000  # Returns HTML

# WebSocket check (requires connection test)
# Run E2E test: cd frontend && bun playwright test

# Database check
docker compose exec postgres psql -U railway -c "SELECT count(*) FROM users;"

# Redis check
docker compose exec redis redis-cli ping  # Returns PONG

# PM2 check
pm2 list  # Shows managed processes

# Traefik check
curl http://localhost:8080/api/rawdata  # Returns Traefik config
```

### Final Checklist

- [ ] All 36 tasks completed
- [ ] All "Must Have" features implemented
- [ ] All "Must NOT Have" items excluded
- [ ] Backend API fully functional
- [ ] Frontend UI matches Railway aesthetic
- [ ] WebSocket log streaming works
- [ ] GitHub OAuth + JWT authentication works
- [ ] PM2 process deployment works
- [ ] Team workspaces with RBAC works
- [ ] SSL certificates auto-provision
- [ ] All tests pass (unit, integration, E2E)
- [ ] Documentation complete
- [ ] CLI tool functional

---

## Guardrails from Metis Review (Self-Review)

**Critical Gaps Addressed**:
1. ✓ Added explicit test infrastructure setup tasks (0.1, 0.2)
2. ✓ Included Redis pub/sub for WebSocket scaling
3. ✓ Specified AES-256-GCM over Fernet for encryption
4. ✓ Added RLS policy placeholders for multi-tenant security
5. ✓ Included graceful shutdown handling in PM2 service
6. ✓ Added backup system (originally missed)
7. ✓ Specified resource quotas enforcement

**AI-Slop Patterns Prevented**:
1. ✓ No Docker for app deployments (explicitly PM2-only)
2. ✓ No Kubernetes references
3. ✓ Real acceptance criteria with commands, not vague statements
4. ✓ No "TODO: implement" placeholders in plan
5. ✓ Explicit file paths for all deliverables
6. ✓ Concrete verification steps, not "user tests"

**Hidden Complexities Addressed**:
1. ✓ PM2 connection lifecycle management
2. ✓ WebSocket reconnection handling
3. ✓ JWT refresh token rotation
4. ✓ Deployment rollback procedures
5. ✓ Health check grace periods
6. ✓ Celery task retry with exponential backoff

---

*Plan generated: 2026-01-30*
*Total Tasks: 36*
*Estimated Duration: 120-150 hours*
*Parallel Efficiency: 55%*
