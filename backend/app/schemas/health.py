from __future__ import annotations

from typing import Literal

from pydantic import BaseModel


class HealthResponse(BaseModel):
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
