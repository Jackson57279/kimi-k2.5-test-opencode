# FastAPI PaaS - Architectural Decisions

## Date: 2026-01-29

### Decision 1: Async-First Architecture
**Rationale**: FastAPI's async support provides better concurrency for I/O-bound operations like Docker API calls and database queries.

### Decision 2: Celery for Background Tasks
**Rationale**: 
- Better than FastAPI BackgroundTasks for long-running operations
- Supports retries, monitoring (Flower), and distributed workers
- Redis broker provides persistence and reliability

### Decision 3: SQLAlchemy 2.0 with Async
**Rationale**:
- Modern ORM with full async support
- Connection pooling critical for high throughput
- Alembic for migrations

### Decision 4: WebSocket for Real-Time Logs
**Rationale**:
- Lower latency than polling
- ConnectionManager pattern scales well
- Heartbeat prevents connection drops

### Decision 5: Fernet Encryption for Env Vars
**Rationale**:
- Simple symmetric encryption
- No external dependencies (HashiCorp Vault optional upgrade)
- Transparent to application code

### Decision 6: Multi-Queue Celery Setup
**Rationale**:
- Separate queues for builds vs deployments
- Different worker configurations per queue
- Prevents build tasks from blocking deployments

### Decision 7: GitHub OAuth Primary Auth
**Rationale**:
- Target users are developers with GitHub accounts
- OAuth2 flow well-documented
- Access to repo webhooks for CI/CD
