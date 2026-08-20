# Architecture

Live Memories is a full-stack app for cataloguing personal concert history: a **FastAPI** backend, a **React + TypeScript** frontend, and **Google Cloud Platform** infrastructure provisioned with Terraform.

---

## System overview

```mermaid
graph TB
    User["User browser"]

    subgraph GCP["Google Cloud Platform"]
        subgraph CloudRun["Cloud Run"]
            Frontend["Frontend service<br/>nginx + React SPA"]
            Backend["Backend service<br/>FastAPI + Uvicorn"]
        end

        SQL[("Cloud SQL<br/>PostgreSQL 16<br/>private IP + TLS")]
        GCS["Cloud Storage<br/>concert photo uploads"]
        SecretManager["Secret Manager<br/>JWT secret, DB password,<br/>admin password"]
        ArtifactRegistry["Artifact Registry<br/>Docker images"]
        VPC["VPC network<br/>private services access"]
    end

    GitHub["GitHub repository"]
    CloudBuild["Cloud Build<br/>build, test, deploy"]

    User -->|HTTPS| Frontend
    Frontend -->|"/api/v1/* proxied"| Backend
    Backend -->|"asyncpg, private IP"| SQL
    Backend -->|signed URLs| GCS
    Backend -.->|reads secrets at startup| SecretManager
    Backend -.-> VPC
    SQL -.-> VPC

    GitHub -->|push to master| CloudBuild
    CloudBuild -->|build & push images| ArtifactRegistry
    CloudBuild -->|deploy| CloudRun
    CloudBuild -->|run migrations job| SQL

    classDef gcp fill:#e8f0fe,stroke:#4285f4,color:#174ea6
    class Frontend,Backend,SQL,GCS,SecretManager,ArtifactRegistry,VPC,CloudBuild gcp
```

---

## Backend – layered architecture

The backend enforces a strict layering so business logic never touches HTTP or SQL concerns directly.

```mermaid
graph LR
    Client["HTTP client"] --> MW["Middleware<br/>CORS, rate limit,<br/>request-ID, security headers"]
    MW --> Endpoints["app/api/v1/endpoints/*<br/>FastAPI routers"]
    Endpoints --> Schemas["app/schemas/*<br/>Pydantic request/response"]
    Endpoints --> Services["app/services/*<br/>business logic"]
    Services --> Repositories["app/repositories/*<br/>SQLAlchemy queries"]
    Repositories --> Models["app/models/*<br/>ORM models"]
    Models --> DB[("PostgreSQL / SQLite")]

    Endpoints -.->|Depends| Security["app/core/security.py<br/>JWT auth"]
    Endpoints -.->|Depends| Session["app/db/session.py<br/>AsyncSession"]
    Services -.-> Exceptions["app/core/exceptions.py<br/>AppError -> JSON envelope"]
    Config["app/core/config.py<br/>Settings (env vars)"] -.-> MW
    Config -.-> Security
    Config -.-> Session
```

**Request flow example — `PUT /api/v1/concerts/{id}`:**

1. Middleware chain: rate limiter → request ID → CORS → security headers.
2. Router validates the path/body against `ConcertUpdate` (Pydantic).
3. `get_current_user` dependency verifies the JWT bearer token.
4. `ConcertService.update_concert()` fetches the entity via `ConcertRepository`, raises `AppError(CONCERT_NOT_FOUND)` if missing.
5. Repository issues an async SQLAlchemy `UPDATE` and re-fetches with eager-loaded relations.
6. Response is serialised through `ConcertResponse` and returned as JSON.

---

## Frontend – component/data flow

```mermaid
graph TB
    Router["React Router<br/>AppRouter"] --> Pages["Pages<br/>ConcertsPage, ConcertDetailPage,<br/>ConcertFormPage, HomePage"]
    Pages --> Hooks["Hooks<br/>useConcerts, useArtists,<br/>useVenues, useAuth"]
    Hooks --> Query["TanStack Query<br/>cache + mutations"]
    Query --> ApiClient["API layer<br/>src/api/* (Axios)"]
    ApiClient -->|"/api/v1"| Backend2["Backend (FastAPI)"]

    Pages --> Forms["React Hook Form<br/>+ Zod-style validation"]
    Pages --> MUI["Material UI<br/>components + theme"]
    Pages --> I18n["i18next<br/>es / en"]
```

---

## Deployment pipeline

```mermaid
sequenceDiagram
    participant Dev as Developer
    participant GH as GitHub
    participant CI as GitHub Actions (CI)
    participant CB as Cloud Build
    participant AR as Artifact Registry
    participant CR as Cloud Run

    Dev->>GH: git push (master)
    GH->>CI: trigger workflow
    CI->>CI: backend: ruff, mypy, pytest --cov
    CI->>CI: frontend: eslint, prettier, tsc, vitest, build
    CI->>CI: docker build (backend + frontend)
    CI->>CI: terraform validate + fmt
    GH->>CB: trigger on push (separate pipeline)
    CB->>CB: run backend tests
    CB->>AR: build & push backend/frontend images (SHORT_SHA tag)
    CB->>CR: deploy new revisions
    CB->>CR: run Alembic migrations job
```

---

## Security boundaries

- **Backend Cloud Run service** is *not* publicly invokable — only the frontend's service account has `roles/run.invoker`.
- **Cloud SQL** has no public IP; reachable only via the VPC with enforced TLS (`ssl_mode = ENCRYPTED_ONLY`).
- **Secrets** (JWT signing key, DB password, admin password) are injected as env vars from **Secret Manager** at container start — never baked into images.
- **JWT auth**: all write endpoints (`POST`/`PUT`/`DELETE`) require a bearer token issued by `POST /api/v1/auth/token`; read endpoints (`GET`) are public.
- **Rate limiting**: in-memory sliding window (120 req/60s per IP), bypassing `/health` and `/ready` so orchestrator probes are never throttled.
- **Docs disabled in production**: `/docs`, `/redoc`, `/openapi.json` only exist when `APP_ENV != production`.

See [SECURITY.md](../SECURITY.md) for the vulnerability disclosure process and [API.md](API.md) for the full endpoint reference.
