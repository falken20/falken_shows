"""Unit tests for the AppError exception and ErrorCode."""

from __future__ import annotations

from app.core.exceptions import AppError, ErrorCode


def test_app_error_default_message() -> None:
    err = AppError(ErrorCode.CONCERT_NOT_FOUND, status_code=404)
    assert err.status_code == 404
    assert err.code == ErrorCode.CONCERT_NOT_FOUND
    assert "not found" in err.message.lower()


def test_app_error_custom_message() -> None:
    err = AppError(ErrorCode.NOT_FOUND, message="Custom message", status_code=404)
    assert err.message == "Custom message"


def test_app_error_to_dict() -> None:
    err = AppError(ErrorCode.VALIDATION_ERROR, status_code=422)
    result = err.to_dict()
    assert "error" in result
    assert result["error"]["code"] == ErrorCode.VALIDATION_ERROR  # type: ignore[index]


def test_app_error_details() -> None:
    err = AppError(ErrorCode.NOT_FOUND, status_code=404, details={"field": "id"})
    assert err.details == {"field": "id"}


def test_error_code_values() -> None:
    assert ErrorCode.CONCERT_NOT_FOUND == "CONCERT_NOT_FOUND"
    assert ErrorCode.UNAUTHORIZED == "UNAUTHORIZED"
    assert ErrorCode.INVALID_FILE_TYPE == "INVALID_FILE_TYPE"
