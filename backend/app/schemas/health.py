from __future__ import annotations

from typing import Literal

from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Response schema for ``GET /api/v1/health``.

    Intentionally omits environment and version to avoid reconnaissance.
    """

    status: Literal["ok", "degraded", "error"]

    model_config = {
        "json_schema_extra": {
            "example": {
                "status": "ok",
            }
        }
    }


class ReadinessResponse(BaseModel):
    """Response schema for ``GET /api/v1/ready``.

    Attributes:
        status: Overall readiness. ``ok`` when all dependencies are healthy;
            ``error`` when the database probe fails.
        database: Result of the database connectivity probe
            (``SELECT 1``). ``ok`` or ``error``.
    """

    status: Literal["ok", "error"]
    database: Literal["ok", "error"]

    model_config = {
        "json_schema_extra": {
            "example": {
                "status": "ok",
                "database": "ok",
            }
        }
    }
