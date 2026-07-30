# Architecture Decision Record – ADR-003

## Title: SQLite for local development and PostgreSQL for production

**Status**: Accepted  
**Date**: 2026-07-15  
**Context**: Live Memories

---

## Context

The application needs a relational database. The requirements are:

- Easy local development without Docker/services.
- Production-grade persistence on GCP.
- No code changes required to switch databases.

## Decision

Use **SQLite** as the default development database and **PostgreSQL** for production. The database is selected via the `DATABASE_URL` environment variable.

## Rationale

- **Developer experience**: SQLite requires zero configuration and runs in-file, enabling immediate local development.
- **Test isolation**: SQLite in-memory databases provide fast, isolated test runs.
- **Production reliability**: PostgreSQL is the industry-standard relational database with ACID compliance, excellent performance, and Cloud SQL support on GCP.
- **SQLAlchemy 2**: Provides a database-agnostic ORM that works with both SQLite and PostgreSQL.
- **No code changes**: A single `DATABASE_URL` environment variable switches the database driver and connection.
- **Alembic migrations**: Work with both databases via `render_as_batch=True` for SQLite compatibility.

## Constraints

- Migrations must use `render_as_batch=True` in Alembic for SQLite ALTER TABLE support.
- Dialect-specific SQL (e.g., PostgreSQL-specific types) must be documented and wrapped conditionally.
- Test suite uses SQLite in-memory; all tests must pass on both dialects.

## Consequences

- Local development requires no running database service.
- CI tests run with SQLite in-memory.
- Production deployments use Cloud SQL PostgreSQL.
- The `DATABASE_URL` environment variable is the only required change to switch environments.

## Example

```env
# Development
DATABASE_URL=sqlite:///./data/live_memories.db

# Production
DATABASE_URL=postgresql+psycopg2://user:password@host:5432/live_memories
```
