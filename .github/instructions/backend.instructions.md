---
applyTo: "backend/**/*.py"
---

# Backend Python Instructions

## Architecture rules

- Follow the strict layered architecture:
  - `app/api/v1/endpoints/` – FastAPI routers: validation in, response out. No business logic.
  - `app/services/` – Business logic. No direct DB access (use repositories).
  - `app/repositories/` – All SQLAlchemy queries. No business logic. Repositories should return `None` on not-found; services are responsible for raising `AppError(ErrorCode.X_NOT_FOUND)`.
  - `app/models/` – SQLAlchemy ORM models only.
  - `app/schemas/` – Pydantic 2 models for request/response. Name schemas as `<Entity>Create`, `<Entity>Update`, `<Entity>Response`.
  - `app/core/` – Config, security, logging, exceptions.

## Migrations

- Use Alembic for all schema changes.
- Never modify the database schema manually.

## Python style

- Python 3.11+ syntax: `X | None`, `match/case`, modern generics `list[str]`, `dict[str, int]`.
- All functions and methods require type annotations (enforced by Mypy strict).
- Line length: 120 characters (Ruff).
- No `# type: ignore` without an explanatory comment on the same line.
- Use `Annotated[..., Depends(...)]` for FastAPI dependency injection.

## SQLAlchemy 2

- Always use async sessions: `AsyncSession`.
- Never use `SELECT *` – always list columns explicitly.
- Avoid N+1 queries: use `selectinload` or `joinedload` where appropriate.
- Use `text()` for raw SQL only for complex aggregations or window functions not supported by SQLAlchemy Core/ORM; parameterise all values.

## Error handling

```python
from app.core.exceptions import AppError, ErrorCode
raise AppError(ErrorCode.CONCERT_NOT_FOUND, status_code=404)
```

- Never return raw `Exception` objects.
- Never swallow exceptions silently.

## Security

- Sanitise and validate all inputs through Pydantic schemas.
- Never log passwords, tokens, or sensitive field values.
- Validate file uploads: MIME type (Pillow), file size, filename sanitisation.
- Use parameterised queries exclusively.

## Commands

```bash
cd backend
uv run ruff check app tests    # Lint
uv run ruff format app tests   # Format
uv run mypy app                # Type check
uv run pytest --cov=app        # Tests with coverage
```
