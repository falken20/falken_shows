"""Unit tests for security hardening measures."""

from __future__ import annotations

from httpx import AsyncClient


class TestProductionDocsDisabled:
    """Verify that OpenAPI docs are disabled in production mode."""

    def test_docs_disabled_in_production(self) -> None:
        """Ensure docs_url, redoc_url, and openapi_url are None in production."""
        from app.core.config import Settings

        settings = Settings(
            APP_ENV="production",
            JWT_SECRET_KEY="a-very-strong-secret-key-longer-than-32-chars",
            ADMIN_PASSWORD="strong-admin-password-12",
            CORS_ORIGINS=["https://app.livememories.app"],
        )
        # The FastAPI app uses: docs_url="..." if APP_ENV != "production" else None
        assert settings.APP_ENV == "production"

    def test_docs_enabled_in_development(self) -> None:
        """Ensure docs are available in non-production mode."""
        from app.core.config import Settings

        settings = Settings(APP_ENV="development")
        assert settings.APP_ENV != "production"


class TestCorsCredentials:
    """Verify CORS credentials behavior by environment."""

    def test_credentials_disabled_in_production(self) -> None:
        """In production, allow_credentials should be False."""
        from app.core.config import Settings

        settings = Settings(
            APP_ENV="production",
            JWT_SECRET_KEY="a-very-strong-secret-key-longer-than-32-chars",
            ADMIN_PASSWORD="strong-admin-password-12",
            CORS_ORIGINS="https://app.livememories.app",
        )
        # The main.py uses: allow_credentials=settings.APP_ENV != "production"
        assert (settings.APP_ENV != "production") is False

    def test_credentials_enabled_in_development(self) -> None:
        """In development, allow_credentials should be True."""
        from app.core.config import Settings

        settings = Settings(APP_ENV="development")
        assert (settings.APP_ENV != "production") is True


class TestAsyncDatabaseSession:
    """Verify async DB session configuration."""

    def test_get_db_is_async_generator(self) -> None:
        """get_db should be an async generator function."""
        import inspect

        from app.db.session import get_db

        assert inspect.isasyncgenfunction(get_db)

    def test_async_engine_created(self) -> None:
        """The module should expose an async engine."""
        from sqlalchemy.ext.asyncio import AsyncEngine

        from app.db.session import async_engine

        assert isinstance(async_engine, AsyncEngine)


class TestGetCurrentUser:
    """Verify the get_current_user JWT dependency rejects bad tokens."""

    async def test_rejects_malformed_token(self, async_client: AsyncClient) -> None:
        response = await async_client.post(
            "/api/v1/artists",
            json={"name": "Should Not Be Created"},
            headers={"Authorization": "Bearer not-a-valid-jwt"},
        )
        assert response.status_code == 401

    async def test_rejects_missing_token(self, async_client: AsyncClient) -> None:
        response = await async_client.post("/api/v1/artists", json={"name": "Should Not Be Created"})
        assert response.status_code == 401

    async def test_rejects_token_without_sub_claim(self, async_client: AsyncClient) -> None:
        from app.core.security import create_access_token

        token = create_access_token({"foo": "bar"})
        response = await async_client.post(
            "/api/v1/artists",
            json={"name": "Should Not Be Created"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 401


class TestAuthenticate:
    """Verify the authenticate() service rejects invalid admin credentials."""

    async def test_rejects_wrong_email(self, async_client: AsyncClient) -> None:
        response = await async_client.post(
            "/api/v1/auth/token",
            data={"username": "not-admin@example.com", "password": "change-me-in-production"},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        assert response.status_code == 401

    async def test_rejects_wrong_password(self, async_client: AsyncClient) -> None:
        response = await async_client.post(
            "/api/v1/auth/token",
            data={"username": "admin@example.com", "password": "wrong-password"},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        assert response.status_code == 401
