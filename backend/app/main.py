from __future__ import annotations

import logging
import time
import uuid
from collections import defaultdict
from collections.abc import AsyncGenerator, Awaitable, Callable
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.exceptions import AppError, app_error_handler
from app.core.logging import configure_logging
from app.db.session import create_db_and_tables

configure_logging()
logger = logging.getLogger(__name__)

# ── In-memory rate limiter (sliding window) ────────────────────
# Stores {ip: [timestamp, ...]} for a 60-second rolling window.
_rate_limit_store: dict[str, list[float]] = defaultdict(list)
_RATE_LIMIT_MAX = 120   # requests per window
_RATE_LIMIT_WINDOW = 60  # seconds
_RATE_LIMIT_EXCLUDED_PATHS = {
    "/api/v1/health",
    "/api/v1/ready",
}


@asynccontextmanager
async def lifespan(application: FastAPI) -> AsyncGenerator[None, None]:
    """FastAPI lifespan handler: runs startup logic before yield, teardown after.

    Startup:
        - Creates DB tables when running with SQLite (development / CI).
        - Logs app name, version, and environment so the first log line is
          always useful for debugging cloud deployments.

    In production, DB tables are managed by Alembic migrations, so
    ``create_db_and_tables`` is effectively a no-op against PostgreSQL.
    """
    logger.info("startup app=%s version=%s env=%s", settings.APP_NAME, settings.APP_VERSION, settings.APP_ENV)
    create_db_and_tables()
    yield
    logger.info("shutdown")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Personal concert inventory API",
    docs_url="/docs" if settings.APP_ENV != "production" else None,
    redoc_url="/redoc" if settings.APP_ENV != "production" else None,
    openapi_url="/openapi.json" if settings.APP_ENV != "production" else None,
    lifespan=lifespan,
)

app.add_exception_handler(AppError, app_error_handler)  # type: ignore[arg-type]

# ── CORS ──────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.APP_ENV != "production",
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Accept", "Origin", "X-Requested-With"],
)


# ── Rate limiting middleware ───────────────────────────────────
@app.middleware("http")
async def rate_limit(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    """Sliding-window rate limiter: 120 requests per 60 seconds per IP.

    Maintains an in-memory list of request timestamps per client IP.  Old
    entries outside the rolling window are pruned on every request to keep
    memory bounded.  Returns HTTP 429 with a ``Retry-After`` header when the
    limit is exceeded.

    Note:
        This limiter is per-process. In multi-replica deployments, consider
        replacing it with a Redis-backed solution (e.g. via limits library).
    """
    if request.url.path in _RATE_LIMIT_EXCLUDED_PATHS:
        return await call_next(request)

    client_ip = request.client.host if request.client else "unknown"
    now = time.time()
    window_start = now - _RATE_LIMIT_WINDOW

    # Prune old entries
    timestamps = _rate_limit_store[client_ip]
    _rate_limit_store[client_ip] = [t for t in timestamps if t > window_start]

    if len(_rate_limit_store[client_ip]) >= _RATE_LIMIT_MAX:
        return JSONResponse(
            status_code=429,
            content={"error": {"code": "RATE_LIMIT_EXCEEDED", "message": "Too many requests", "details": {}}},
            headers={"Retry-After": str(_RATE_LIMIT_WINDOW)},
        )

    _rate_limit_store[client_ip].append(now)
    return await call_next(request)


# ── Request ID middleware ──────────────────────────────────────
@app.middleware("http")
async def add_request_id(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    """Attach a unique ``X-Request-ID`` header to every response.

    Clients and log aggregators can use this UUID to correlate frontend errors
    with backend log entries across distributed traces.
    """
    request_id = str(uuid.uuid4())
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response


# ── Security headers middleware ────────────────────────────────
@app.middleware("http")
async def add_security_headers(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    """Inject OWASP-recommended security response headers on every request.

    Headers applied to all environments:
        - ``X-Content-Type-Options: nosniff`` – prevents MIME-type sniffing.
        - ``X-Frame-Options: DENY`` – blocks the API being embedded in iframes.
        - ``Referrer-Policy`` – limits referrer leakage across origins.
        - ``Content-Security-Policy`` – restrictive policy for an API (no browser assets).
        - ``Permissions-Policy`` – disables unnecessary browser features.

    Additionally in production:
        - ``Strict-Transport-Security`` – enforces HTTPS for two years with preload.
    """
    response = await call_next(request)

    # Baseline hardening headers for API responses.
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Content-Security-Policy"] = "default-src 'none'; frame-ancestors 'none'; base-uri 'none'"
    response.headers["Permissions-Policy"] = "geolocation=(), camera=(), microphone=()"

    if settings.APP_ENV == "production":
        response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains; preload"

    return response


# ── Routers ────────────────────────────────────────────────────
app.include_router(api_router, prefix="/api/v1")


# ── Global exception handler ───────────────────────────────────
@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Last-resort handler for unhandled exceptions.

    Logs the full traceback (request path + exception) and returns a generic
    500 response using the standard error envelope.  Avoids leaking internal
    stack traces to API consumers.
    """
    logger.error("unhandled_exception path=%s error=%s", request.url.path, exc, exc_info=exc)
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred",
                "details": {},
            }
        },
    )
