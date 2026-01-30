# FastAPI PaaS Research - Key Learnings

## Date: 2026-01-29

### Docker Multi-Tenant Patterns
- Use non-root containers for security
- Implement resource quotas (CPU/memory limits)
- Use docker-socket-proxy for secure Docker API access
- Multi-stage builds reduce image size significantly
- Health checks essential for orchestration

### WebSocket Log Streaming
- ConnectionManager pattern handles multiple clients per deployment
- Heartbeat mechanism (30s interval) keeps connections alive
- Broadcast pattern sends logs to all connected clients
- Docker SDK provides streaming log access with follow=True
- Connection limits prevent resource exhaustion (100 per deployment)

### SQLAlchemy ORM Patterns
- Async SQLAlchemy 2.0 with asyncpg driver for PostgreSQL
- Repository pattern abstracts data access
- Connection pooling critical: pool_size=20, max_overflow=30
- expire_on_commit=False improves FastAPI performance
- Multi-tenant queries must always include tenant_id filter

### Celery + Redis Job Queue
- Separate queues for different task types (build, deploy)
- Task routing ensures proper worker allocation
- DatabaseTask base class provides session management
- Retry with exponential backoff for transient failures
- Soft time limits allow graceful shutdown

### GitHub OAuth + JWT
- Use authlib for OAuth2 integration
- JWT access tokens (short-lived) + refresh tokens (long-lived)
- HTTP-only cookies for refresh tokens prevent XSS
- GitHub user/emails endpoint for verified email
- Token type claim distinguishes access vs refresh

### Environment Variable Encryption
- Fernet symmetric encryption for at-rest protection
- Master key derivation using PBKDF2HMAC
- Encrypted values prefixed with "encrypted:"
- Alternative: HashiCorp Vault for enterprise
- Never log decrypted values

### Webhook Security
- Always verify signatures (HMAC-SHA256)
- Process webhooks in background tasks
- Return 200 quickly to prevent retries
- Store secrets per-deployment
- Support multiple providers (GitHub, GitLab)

## Library Versions (Production-Ready)
- FastAPI: ^0.115
- SQLAlchemy: ^2.0
- Celery: ^5.4
- python-jose: ^3.3
- cryptography: ^44.0
- docker-py: ^7.1
