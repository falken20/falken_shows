from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.session import get_db
from app.schemas.health import HealthResponse, ReadinessResponse

router = APIRouter()


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
    description="Returns a 200 response if the service is running.",
)
async def health_check() -> HealthResponse:
    """Lightweight liveness probe for load balancers and uptime monitors.

    Does **not** check database connectivity – use ``/ready`` for that.
    Safe to call at high frequency; no I/O is performed.
    """
    return HealthResponse(
        status="ok",
        app_name=settings.APP_NAME,
        version=settings.APP_VERSION,
        environment=settings.APP_ENV,
    )


@router.get(
    "/ready",
    response_model=ReadinessResponse,
    summary="Readiness check",
    description="Returns 200 if the service is ready to serve requests (DB connection OK).",
)
async def readiness_check(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ReadinessResponse:
    """Readiness probe used by Cloud Run and Kubernetes to gate traffic.

    Executes a trivial ``SELECT 1`` against the database to verify that the
    connection pool is healthy.  Returns ``status=degraded`` instead of
    raising an HTTP 500 so the orchestrator receives a parseable response.
    """
    try:
        await db.execute(text("SELECT 1"))
        db_status = "ok"
    except Exception:
        db_status = "error"

    overall = "ok" if db_status == "ok" else "degraded"

    return ReadinessResponse(status=overall, database=db_status)
