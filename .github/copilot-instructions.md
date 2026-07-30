# Live Memories – Copilot Instructions

This file provides GitHub Copilot with context about the Live Memories project so that suggestions are consistent with the architecture, conventions, and quality standards of the codebase.

---

## Project overview

Live Memories is a full-stack web application for cataloguing personal concert experiences. It uses a **FastAPI** backend and a **React + TypeScript** frontend organised as a monorepo.

```
live-memories/
├── backend/    # Python 3.12 + FastAPI + SQLAlchemy 2 + Alembic
├── frontend/   # React 18 + TypeScript + Vite + Material UI
├── infrastructure/  # Terraform + Cloud Build
└── docs/       # ADRs and architecture docs
```

---

## Python conventions (backend)

- Python 3.12+. Use modern syntax: `X | None`, `match`, `TypeAlias`.
- Use **async/await** for all database access and I/O.
- Follow the layered architecture strictly:
  - `app/api/v1/endpoints/` – FastAPI routers, only input/output handling
  - `app/services/` – business logic, no DB access
  - `app/repositories/` – all database queries via SQLAlchemy
  - `app/models/` – SQLAlchemy ORM models
  - `app/schemas/` – Pydantic 2 request/response models
  - `app/core/` – config, security, logging
- All functions must have type annotations.
- Use `Annotated` for dependency injection.
- Format with **Ruff Format** (line length 120). Lint with **Ruff**.
- Type-check with **Mypy** in strict mode.
- Never use `# type: ignore` without a comment explaining why.

### Adding an endpoint

1. Create or update the router in `app/api/v1/endpoints/<resource>.py`.
2. Create the Pydantic schemas in `app/schemas/<resource>.py`.
3. Implement business logic in `app/services/<resource>_service.py`.
4. Implement data access in `app/repositories/<resource>_repository.py`.
5. Register the router in `app/api/v1/router.py`.
6. Write integration tests in `backend/tests/integration/test_<resource>.py`.

### Adding a migration

```bash
# After modifying a SQLAlchemy model:
make migrate-create MSG="describe the change"
# Review the generated file, then:
make migrate
```

Migrations must work with both SQLite and PostgreSQL. Use `op.execute()` only if absolutely necessary and document dialect-specific code.

### Error handling

Use the shared error response model:
```python
from app.core.exceptions import AppError, ErrorCode

raise AppError(ErrorCode.CONCERT_NOT_FOUND, status_code=404)
```

Never return raw exceptions or unformatted error strings.

---

## TypeScript conventions (frontend)

- React 18 with functional components only. No class components.
- TypeScript strict mode. No `any` unless justified with a comment.
- Use **TanStack Query** for all server state. Never use raw `fetch` in components.
- Use **React Hook Form + Zod** for all forms.
- Use **React Router v6** with typed `useParams` and `useNavigate`.
- Use **Material UI** components. Extend with `sx` prop or `styled()`.
- Export one component per file. File name = component name (PascalCase).
- Hooks go in `src/hooks/`. API clients in `src/api/`. Types in `src/types/`.
- Use `i18next` for all user-facing strings. Never hardcode strings.

### Adding a component

1. Create `src/components/<Category>/<ComponentName>.tsx`
2. Create `src/components/<Category>/<ComponentName>.test.tsx`
3. Export from `src/components/<Category>/index.ts`

### Adding a page

1. Create `src/pages/<PageName>/<PageName>.tsx`
2. Add the route in `src/router/index.tsx`
3. Add navigation entry if needed

---

## Testing conventions

### Backend

- Use **Pytest** with `asyncio_mode = "auto"` (configured in `pyproject.toml`).
- Use a SQLite in-memory database for tests (configured via `conftest.py`).
- Every endpoint must have at least: happy path, validation error, not found.
- Use `factory_boy` or simple helper functions for test data – no hardcoded IDs.
- Coverage must stay ≥ 80 %.

### Frontend

- Use **Vitest + React Testing Library**.
- Mock API calls with **MSW** (configured in `src/mocks/`).
- Test user behaviour, not implementation details.
- Avoid `getByTestId` – prefer accessible queries (`getByRole`, `getByLabelText`).

---

## Error handling rules

- Never swallow exceptions silently.
- Log errors with context (request ID, user ID if available).
- Return appropriate HTTP status codes.
- Frontend must handle and display API errors gracefully.

---

## Documentation

- Add docstrings only to public functions and classes where the purpose is not obvious from the name and signature.
- Keep comments focused on *why*, not *what*.
- Update `CHANGELOG.md` for every notable change.

---

## Secrets management

- **Never commit secrets** (API keys, passwords, tokens, private keys).
- Use `.env.example` for documentation. Use `.env` (gitignored) for local development.
- In production, use **Google Secret Manager**.
- Access secrets via environment variables loaded in `app/core/config.py`.
- No secret should appear in logs.

---

## Commands to run before finishing changes

```bash
make format      # Auto-format all code
make lint        # Fix linting issues
make typecheck   # Type checking
make test        # All tests must pass
```

---

## Hard rules – Copilot must follow these

1. **Never disable tests** to make a build pass.
2. **Never add dependencies** without justifying them in the PR description.
3. **Always maintain compatibility** with both SQLite and PostgreSQL.
4. **Always preserve frontend accessibility**: keyboard navigation, ARIA labels, alt text.
5. **Never include credentials**, tokens, or real personal data in code or tests.
6. **Never use `SELECT *`** in SQLAlchemy queries.
7. **Always paginate** list endpoints – never return unbounded collections.
8. **Never bypass CORS or security middleware**.
9. **Always validate file uploads** (type, size) before processing.
10. **Follow Conventional Commits** for all commit messages.
