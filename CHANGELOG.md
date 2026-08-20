# Changelog

All notable changes to Live Memories will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
- Initial project scaffold with FastAPI backend and React frontend
- Health check and readiness check endpoints
- Docker Compose setup for local development
- GitHub Actions CI workflow
- Copilot instructions and specialised agents
- Architectural Decision Records (ADR-001 through ADR-006)

### Changed
- Migrated database layer from synchronous SQLAlchemy engine to fully async
  `AsyncEngine` / `AsyncSession` (`sqlalchemy[asyncio]`, `aiosqlite`, `asyncpg`).
- Test fixtures in `conftest.py` updated to use `async_sessionmaker` with
  in-memory SQLite (`sqlite+aiosqlite:///:memory:`).
- `get_db` FastAPI dependency is now an async generator.

### Security
- **CRITICAL** – Removed `allUsers` IAM binding from Cloud Run backend service;
  backend now requires service-account authentication
  (`google_cloud_run_v2_service_iam_member` with frontend SA as invoker).
- **CRITICAL** – Database password no longer interpolated into Cloud Run env var;
  all three secrets (JWT, DB password, admin password) injected via
  `secret_key_ref` in Terraform.
- **HIGH** – Cloud SQL public IP disabled (`ipv4_enabled = false`); instance
  now reachable only via VPC private network with `require_ssl = true`.
- **HIGH** – Updated `react-router-dom` to `^7.18.0` (CVE-2025-68470 /
  GHSA-337j-9hxr-rhxg). Updated Vite to `^6.4.3` (esbuild GHSA-67mh-4wv8-2f99).
- **HIGH** – Pinned Python dependencies to patched minimum versions:
  `cryptography>=44.0.0`, `starlette>=0.45.3`, `python-multipart>=0.0.20`,
  `fastapi>=0.115.12`.
- **HIGH** – Removed mutable `:latest` Docker image tags from Cloud Build
  pipeline; only `${SHORT_SHA}`-tagged images are pushed and deployed.
- **MEDIUM** – OpenAPI docs (`/docs`, `/redoc`, `/openapi.json`) disabled when
  `APP_ENV=production`.
- **MEDIUM** – `allow_credentials` set to `False` in production CORS config.
- **MEDIUM** – Added `Content-Security-Policy`, `Strict-Transport-Security`, and
  `Permissions-Policy` headers to Nginx frontend config.
- **MEDIUM** – All GitHub Actions steps pinned by full commit SHA instead of
  mutable version tags (supply-chain hardening).
- **LOW** – SECURITY.md vulnerability disclosure contact updated from placeholder
  to `security@livememories.app`.

### Added (documentation)
- Google-style docstrings added to all public backend modules:
  `config.py`, `exceptions.py`, `logging.py`, `session.py`, `main.py`,
  `router.py`, `health.py` endpoint, `health.py` schemas.
- TSDoc/JSDoc comments added to all frontend modules:
  `client.ts`, `health.ts`, `App.tsx`, `AppRouter.tsx`, `MainLayout.tsx`,
  `TopBar.tsx`, `LoadingFallback.tsx`, `HomePage.tsx`, `NotFoundPage.tsx`,
  `useHealth.ts`, `useThemeMode.tsx`, `theme.ts`, `i18n/index.ts`,
  `test/utils.tsx`, MSW `handlers.ts`, `server.ts`, `browser.ts`.

---

## [0.1.0] - 2026-07-15

### Added
- Repository initialisation
- Project structure and tooling configuration
