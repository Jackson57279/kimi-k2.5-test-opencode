# Railway PaaS Clone - Architectural Decisions

## Decisions Made

### 1. Process-based vs Docker Deployments
**Decision**: Use PM2 process manager, not Docker
**Rationale**: User explicitly requested process-based deployment
**Date**: 2026-01-30

### 2. Single Git Provider
**Decision**: GitHub only for MVP
**Rationale**: Covers 90% of use cases, simpler implementation
**Date**: 2026-01-30

### 3. Encryption Algorithm
**Decision**: AES-256-GCM (not Fernet)
**Rationale**: Superior security, recommended by research
**Date**: 2026-01-30

### 4. Database
**Decision**: PostgreSQL only (no MySQL/MongoDB)
**Rationale**: Simpler MVP, can add later
**Date**: 2026-01-30

### 5. Frontend State Management
**Decision**: Zustand for client state, React Query for server state
**Rationale**: Lightweight, TypeScript-friendly
**Date**: 2026-01-30

## Pending Decisions

