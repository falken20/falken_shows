from __future__ import annotations

from enum import StrEnum

from fastapi import Request
from fastapi.responses import JSONResponse


class ErrorCode(StrEnum):
    """Stable, machine-readable error identifiers returned in every API error response.

    Values are intentionally uppercase strings so they can be matched by clients
    without coupling to HTTP status codes.
    """
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"
    NOT_FOUND = "NOT_FOUND"
    CONCERT_NOT_FOUND = "CONCERT_NOT_FOUND"
    ARTIST_NOT_FOUND = "ARTIST_NOT_FOUND"
    VENUE_NOT_FOUND = "VENUE_NOT_FOUND"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    DUPLICATE_CONCERT = "DUPLICATE_CONCERT"
    UNAUTHORIZED = "UNAUTHORIZED"
    FORBIDDEN = "FORBIDDEN"
    INVALID_FILE_TYPE = "INVALID_FILE_TYPE"
    FILE_TOO_LARGE = "FILE_TOO_LARGE"
    IMPORT_ERROR = "IMPORT_ERROR"


class AppError(Exception):
    """Domain exception raised by services and repositories.

    Centralises error shape so all API error responses share the same JSON
    envelope::

        {"error": {"code": "...", "message": "...", "details": {}}}

    Args:
        code: One of the ``ErrorCode`` enum values.
        message: Human-readable description. Defaults to a title-cased version
            of the error code.
        status_code: HTTP status to return. Defaults to 400.
        details: Optional key-value pairs for machine-readable context
            (e.g. field names, resource IDs).
    """
    def __init__(
        self,
        code: ErrorCode,
        message: str | None = None,
        status_code: int = 400,
        details: dict[str, object] | None = None,
    ) -> None:
        self.code = code
        self.message = message or code.value.replace("_", " ").capitalize()
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)

    def to_dict(self) -> dict[str, object]:
        """Serialise to the standard error envelope consumed by FastAPI responses."""
        return {
            "error": {
                "code": self.code,
                "message": self.message,
                "details": self.details,
            }
        }


async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    """FastAPI exception handler that converts ``AppError`` to a JSON response.

    Register with::

        app.add_exception_handler(AppError, app_error_handler)
    """
    return JSONResponse(status_code=exc.status_code, content=exc.to_dict())
