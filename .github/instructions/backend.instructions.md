---
applyTo: "backend/**/*.py"
---

# Backend Python Instructions

## Architecture rules

- Follow the strict layered architecture:
  - `app/api/v1/endpoints/` – FastAPI routers: validation in, response out. No business logic.
  - `app/services/` – Business logic. No direct DB access (use repositories).
  - `app/repositories/` – All SQLAlchemy queries. No business logic.
  - `app/models/` – SQLAlchemy ORM models only.
  - `app/schemas/` – Pydantic 2 models for request/response.
  - `app/core/` – Config, security, logging, exceptions.

## Python style

- Python 3.12+ syntax: `X | None`, `match/case`, modern generics `list[str]`, `dict[str, int]`.
- All functions and methods require type annotations (enforced by Mypy strict).
- Line length: 120 characters (Ruff).
- No `# type: ignore` without an explanatory comment on the same line.
- Use `Annotated[..., Depends(...)]` for FastAPI dependency injection.

## SQLAlchemy 2

- Always use async sessions: `AsyncSession`.
- Never use `SELECT *` – always list columns explicitly.
- Avoid N+1 queries: use `selectinload` or `joinedload` where appropriate.
- Use `text()` for raw SQL only when unavoidable; parameterise all values.

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
