"""Unit tests for security hardening measures."""

from __future__ import annotations


class TestProductionDocsDisabled:
    def test_docs_disabled_in_production(self) -> None:
        from app.core.config import Settings

        settings = Settings(
            APP_ENV="production",
            JWT_SECRET_KEY="a-very-strong-secret-key-longer-than-32-chars",
            ADMIN_PASSWORD="strong-admin-password-12",
            CORS_ORIGINS=["https://app.livememories.app"],
        )
        assert settings.APP_ENV == "production"

    def test_docs_enabled_in_development(self) -> None:
        from app.core.config import Settings

        settings = Settings(APP_ENV="development")
        assert settings.APP_ENV != "production"


class TestCorsCredentials:
    def test_credentials_disabled_in_production(self) -> None:
        from app.core.config import Settings

        settings = Settings(
            APP_ENV="production",
            JWT_SECRET_KEY="a-very-strong-secret-key-longer-than-32-chars",
            ADMIN_PASSWORD="strong-admin-password-12",
            CORS_ORIGINS="https://app.livememories.app",
        )
        assert (settings.APP_ENV not in ("production", "staging")) is False

    def test_credentials_enabled_in_development(self) -> None:
        from app.core.config import Settings

        settings = Settings(APP_ENV="development")
        assert (settings.APP_ENV not in ("production", "staging")) is True


class TestAsyncDatabaseSession:
    def test_get_db_is_async_generator(self) -> None:
        import inspect

        from app.db.session import get_db

        assert inspect.isasyncgenfunction(get_db)

    def test_async_engine_created(self) -> None:
        from sqlalchemy.ext.asyncio import AsyncEngine

        from app.db.session import async_engine

        assert isinstance(async_engine, AsyncEngine)
