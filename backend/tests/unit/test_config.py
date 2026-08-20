"""Unit tests for the application settings/config module."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from app.core.config import Settings


def test_default_app_name() -> None:
    settings = Settings()
    assert settings.APP_NAME == "Live Memories"


def test_default_database_url_is_sqlite() -> None:
    settings = Settings()
    assert "sqlite" in settings.DATABASE_URL


def test_allowed_image_types_list() -> None:
    settings = Settings(ALLOWED_IMAGE_TYPES="image/jpeg,image/png")
    types = settings.allowed_image_types_list
    assert "image/jpeg" in types
    assert "image/png" in types
    assert len(types) == 2


def test_max_upload_size_bytes() -> None:
    settings = Settings(MAX_UPLOAD_SIZE_MB=5)
    assert settings.max_upload_size_bytes == 5 * 1024 * 1024


def test_cors_origins_parsed_from_string() -> None:
    settings = Settings(CORS_ORIGINS="http://localhost:3000,http://localhost:5173")
    assert "http://localhost:3000" in settings.CORS_ORIGINS
    assert "http://localhost:5173" in settings.CORS_ORIGINS


def test_cors_origins_rejects_wildcard() -> None:
    with pytest.raises(ValidationError):
        Settings(CORS_ORIGINS=["*"])


def test_access_token_expiry_must_be_positive() -> None:
    with pytest.raises(ValidationError):
        Settings(ACCESS_TOKEN_EXPIRE_MINUTES=0)


def test_production_requires_strong_jwt_secret() -> None:
    with pytest.raises(ValidationError):
        Settings(APP_ENV="production", JWT_SECRET_KEY="change-me")


def test_production_requires_strong_admin_password() -> None:
    with pytest.raises(ValidationError):
        Settings(APP_ENV="production", ADMIN_PASSWORD="change-me")
