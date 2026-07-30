# Architecture – Live Memories

## Overview

Live Memories is a full-stack web application structured as a monorepo. It consists of a React SPA frontend and a FastAPI REST API backend, communicating over HTTP/JSON.

```
┌─────────────────────────────────────────────────────────┐
│                        Browser                          │
│                                                         │
│  React 18 + Vite + TypeScript + Material UI             │
│  TanStack Query │ React Hook Form │ i18next             │
└─────────────────────────┬───────────────────────────────┘
                           │ HTTP/JSON
                           ▼
┌─────────────────────────────────────────────────────────┐
│                    FastAPI Backend                       │
│                                                         │
│  Router → Service → Repository → SQLAlchemy Model       │
│  Pydantic v2 schemas │ JWT auth │ Alembic migrations     │
└─────────────────────────┬───────────────────────────────┘
                           │
              ┌────────────┴─────────────┐
              ▼                          ▼
    SQLite (development)         Cloud SQL PostgreSQL
                                   (production)
```

---

## Backend architecture

The backend follows a strict layered architecture:

```
app/
├── api/v1/endpoints/   # FastAPI routers – HTTP in/out only
├── services/           # Business logic – no DB access
├── repositories/       # Database queries via SQLAlchemy
├── models/             # SQLAlchemy ORM models
├── schemas/            # Pydantic v2 request/response models
├── core/               # Config, security, logging, exceptions
└── db/                 # Session factory, Base class
```

### Request flow

1. HTTP request arrives at the FastAPI router.
2. Router validates input via Pydantic schema and calls the service.
3. Service contains business logic and calls repository methods.
4. Repository executes SQLAlchemy queries and returns ORM models.
5. Router serialises the result to a Pydantic response schema.

### Database strategy

- **Development/testing**: SQLite via `aiosqlite` driver.
- **Production**: PostgreSQL via `asyncpg` driver.
- Driver is selected via `DATABASE_URL` environment variable.
- Alembic migrations use `render_as_batch=True` for SQLite compatibility.

---

## Frontend architecture

```
src/
├── api/          # Axios client + API module per resource
├── components/   # Reusable UI components
│   ├── common/   # Generic (LoadingFallback, ErrorBoundary, etc.)
│   └── layout/   # Layout components (MainLayout, TopBar, etc.)
├── hooks/        # Custom React hooks
├── i18n/         # Translations (es, en)
├── mocks/        # MSW handlers for testing
├── pages/        # Page components per route
├── router/       # React Router configuration
├── test/         # Test utilities and setup
├── types/        # TypeScript type definitions
└── utils/        # Shared utilities (theme, formatters, etc.)
```

### Data fetching

All server state goes through **TanStack Query**. API calls are defined in `src/api/` modules and consumed by hooks in `src/hooks/`. Components never call `fetch` or `axios` directly.

---

## Security architecture

- **Authentication**: JWT tokens issued by the backend, stored in `httpOnly` cookies or `localStorage` (configurable).
- **Authorisation**: Protected endpoints require `get_current_user` dependency.
- **Passwords**: Bcrypt hashing via `passlib`.
- **CORS**: Explicit allowed origins list; never `*` in production.
- **File uploads**: MIME type validation with Pillow, UUID-based storage keys.
- **Headers**: Security headers applied via FastAPI middleware.
- **Secrets**: Google Secret Manager in production; `.env` locally (never committed).

---

## Image storage

| Environment | Backend | Access |
|---|---|---|
| Local/Dev | Local filesystem | Static file serving |
| Production | Google Cloud Storage | Signed URLs (1h expiry) |

The backend selects the storage implementation via `STORAGE_BACKEND` env var.

---

## Deployment architecture (GCP)

```
  Users
    │
    ▼
Cloud Run (Frontend)       Cloud Run (Backend)
  Nginx + Vite build          FastAPI + Uvicorn
    │                              │
    │                              │
    │                    Cloud SQL (PostgreSQL)
    │                              │
    │                     Cloud Storage (photos)
    │                              │
    │                    Secret Manager (secrets)
    │
Artifact Registry
  (Docker images)
```

CI/CD pipeline (Cloud Build or GitHub Actions):
1. Lint, type-check, test.
2. Build Docker images.
3. Push to Artifact Registry.
4. Run Alembic migrations via Cloud Run Job.
5. Deploy backend Cloud Run service.
6. Deploy frontend Cloud Run service.

---

## Scalability considerations

- **Stateless backend**: Cloud Run instances can scale horizontally.
- **Connection pooling**: PostgreSQL connections are pooled via SQLAlchemy.
- **Caching**: TanStack Query caches server responses on the frontend; add Redis for backend caching when needed.
- **CDN**: Cloud CDN can be added in front of the frontend Cloud Run service for static asset caching.
- **Database**: Cloud SQL can be scaled vertically or migrated to Spanner for extreme scale.

---

## Future decisions

- Multi-user support: Add user table, per-user data isolation.
- Mobile app: React Native sharing API and types with the web frontend.
- Full-text search: PostgreSQL `pg_trgm` or Elasticsearch for concert search.
- Real-time updates: WebSocket support via FastAPI for collaborative features.
