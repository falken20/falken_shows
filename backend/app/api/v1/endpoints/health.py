from __future__ import annotations

import logging
from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.health import HealthResponse, ReadinessResponse

router = APIRouter()
logger = logging.getLogger(__name__)


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
    return HealthResponse(status="ok")


@router.get(
    "/ready",
    response_model=ReadinessResponse,
    summary="Readiness check",
    description="Returns 200 if the service is ready to serve requests (DB connection OK).",
    responses={503: {"model": ReadinessResponse}},
)
async def readiness_check(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> JSONResponse:
    """Readiness probe used by Cloud Run and Kubernetes to gate traffic.

    Executes a trivial ``SELECT 1`` against the database. Returns HTTP 503 when
    the database is unavailable so load balancers stop sending traffic.
    """
    try:
        await db.execute(text("SELECT 1"))
    except Exception:
        try:
            await db.rollback()
        except Exception:
            logger.debug("readiness rollback failed", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content=ReadinessResponse(status="error", database="error").model_dump(),
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=ReadinessResponse(status="ok", database="ok").model_dump(),
    )
