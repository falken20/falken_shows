from __future__ import annotations

from typing import Literal

from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Response schema for ``GET /api/v1/health``.

    Attributes:
        status: Service liveness state. Always ``ok`` when the endpoint
            responds; the value ``degraded`` or ``error`` is reserved for
            future use (e.g. dependency checks).
        app_name: Configured application name (``Settings.APP_NAME``).
        version: Semantic version string from ``Settings.APP_VERSION``.
        environment: Active deployment environment (development / testing / production).
    """

    status: Literal["ok", "degraded", "error"]
    app_name: str
    version: str
    environment: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "status": "ok",
                "app_name": "Live Memories",
                "version": "0.1.0",
                "environment": "development",
            }
        }
    }


class ReadinessResponse(BaseModel):
    """Response schema for ``GET /api/v1/ready``.

    Attributes:
        status: Overall readiness. ``ok`` when all dependencies are healthy;
            ``degraded`` when one or more dependencies are unavailable.
        database: Result of the database connectivity probe
            (``SELECT 1``). ``ok`` or ``error``.
    """

    status: Literal["ok", "degraded", "error"]
    database: Literal["ok", "error"]

    model_config = {
        "json_schema_extra": {
            "example": {
                "status": "ok",
                "database": "ok",
            }
        }
    }
