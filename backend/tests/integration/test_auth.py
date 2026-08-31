"""Integration tests for authentication and JWT handling."""

from __future__ import annotations

import pytest
from httpx import AsyncClient

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
