"""Integration tests for authentication and JWT handling."""

from __future__ import annotations

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

pytestmark = pytest.mark.asyncio


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

    async def test_repeated_failed_logins_are_throttled(self, async_client: AsyncClient) -> None:
        from app.services.auth_service import _LOGIN_MAX_ATTEMPTS

        for _ in range(_LOGIN_MAX_ATTEMPTS):
            response = await async_client.post(
                "/api/v1/auth/token",
                data={"username": "admin@example.com", "password": "wrong-password"},
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )
            assert response.status_code == 401

        response = await async_client.post(
            "/api/v1/auth/token",
            data={"username": "admin@example.com", "password": "wrong-password"},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        assert response.status_code == 429
        assert response.json()["error"]["code"] == "RATE_LIMIT_EXCEEDED"

    async def test_rejects_token_for_non_admin_subject(self, async_client: AsyncClient) -> None:
        from app.core.security import create_access_token

        token = create_access_token({"sub": "other@example.com"})
        response = await async_client.post(
            "/api/v1/artists",
            json={"name": "Should Not Be Created"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 401

    async def test_logout_revokes_token(self, async_client: AsyncClient, auth_token: str) -> None:
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = await async_client.post("/api/v1/auth/logout", headers=headers)
        assert response.status_code == 204

        response = await async_client.get("/api/v1/artists", headers=headers)
        assert response.status_code == 401

    async def test_logout_purges_expired_revocations(
        self, async_client: AsyncClient, auth_token: str, db_session: AsyncSession
    ) -> None:
        from datetime import UTC, datetime, timedelta

        from app.models.auth import RevokedToken

        db_session.add(RevokedToken(jti="expired-jti", expires_at=datetime.now(UTC) - timedelta(minutes=1)))
        await db_session.flush()

        response = await async_client.post(
            "/api/v1/auth/logout",
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        assert response.status_code == 204
        assert await db_session.get(RevokedToken, "expired-jti") is None


class TestCreateConcertWithInvalidFK:
    """Verify that creating a concert with non-existent FK refs is rejected."""

    async def test_create_with_invalid_artist_id(self, async_client: AsyncClient, auth_token: str) -> None:
        response = await async_client.post(
            "/api/v1/concerts",
            json={"title": "Test", "date": "2024-06-15T00:00:00", "artist_id": 99999, "currency": "EUR"},
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        assert response.status_code == 404
        assert response.json()["error"]["code"] == "ARTIST_NOT_FOUND"

    async def test_create_with_invalid_venue_id(self, async_client: AsyncClient, auth_token: str) -> None:
        response = await async_client.post(
            "/api/v1/concerts",
            json={"title": "Test", "date": "2024-06-15T00:00:00", "venue_id": 99999, "currency": "EUR"},
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        assert response.status_code == 404
        assert response.json()["error"]["code"] == "VENUE_NOT_FOUND"
