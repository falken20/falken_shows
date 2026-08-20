"""Integration tests for the /api/v1/concerts endpoints."""
from __future__ import annotations

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from tests.factories import create_artist, create_concert, create_venue

pytestmark = pytest.mark.asyncio


async def _get_token(client: AsyncClient) -> str:
    """Obtain a valid JWT for the default admin user."""
    response = await client.post(
        "/api/v1/auth/token",
        data={"username": "admin@example.com", "password": "change-me-in-production"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200
    return str(response.json()["access_token"])


class TestListConcerts:
    async def test_returns_empty_list_when_no_concerts(self, async_client: AsyncClient) -> None:
        response = await async_client.get("/api/v1/concerts")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0
        assert data["items"] == []

    async def test_returns_concerts(self, async_client: AsyncClient, db_session: AsyncSession) -> None:
        artist = await create_artist(db_session, name="Metallica")
        venue = await create_venue(db_session, name="Wembley", city="London", country="GB")
        await create_concert(db_session, artist=artist, venue=venue, title="Metallica Live")

        response = await async_client.get("/api/v1/concerts")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["items"][0]["title"] == "Metallica Live"

    async def test_pagination_params_are_respected(self, async_client: AsyncClient, db_session: AsyncSession) -> None:
        for i in range(3):
            await create_concert(db_session, title=f"Concert {i}")

        response = await async_client.get("/api/v1/concerts?page=1&page_size=2")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 3
        assert len(data["items"]) == 2


class TestGetConcert:
    async def test_returns_concert(self, async_client: AsyncClient, db_session: AsyncSession) -> None:
        concert = await create_concert(db_session)
        response = await async_client.get(f"/api/v1/concerts/{concert.id}")
        assert response.status_code == 200
        assert response.json()["id"] == concert.id

    async def test_returns_404_for_unknown_id(self, async_client: AsyncClient) -> None:
        response = await async_client.get("/api/v1/concerts/99999")
        assert response.status_code == 404
        assert response.json()["error"]["code"] == "CONCERT_NOT_FOUND"


class TestCreateConcert:
    async def test_creates_concert_with_auth(self, async_client: AsyncClient) -> None:
        token = await _get_token(async_client)
        payload = {"title": "New Concert", "date": "2024-06-15T00:00:00", "currency": "EUR"}
        response = await async_client.post(
            "/api/v1/concerts",
            json=payload,
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 201
        assert response.json()["title"] == "New Concert"

    async def test_create_requires_auth(self, async_client: AsyncClient) -> None:
        payload = {"title": "New Concert", "date": "2024-06-15T00:00:00", "currency": "EUR"}
        response = await async_client.post("/api/v1/concerts", json=payload)
        assert response.status_code == 401

    async def test_create_validates_required_fields(self, async_client: AsyncClient) -> None:
        token = await _get_token(async_client)
        response = await async_client.post(
            "/api/v1/concerts",
            json={},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 422


class TestUpdateConcert:
    async def test_updates_concert_with_auth(self, async_client: AsyncClient, db_session: AsyncSession) -> None:
        concert = await create_concert(db_session, title="Original Title")
        token = await _get_token(async_client)

        response = await async_client.put(
            f"/api/v1/concerts/{concert.id}",
            json={"title": "Updated Title"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        assert response.json()["title"] == "Updated Title"

    async def test_update_returns_404_for_unknown(self, async_client: AsyncClient) -> None:
        token = await _get_token(async_client)
        response = await async_client.put(
            "/api/v1/concerts/99999",
            json={"title": "Updated"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 404


class TestDeleteConcert:
    async def test_deletes_concert_with_auth(self, async_client: AsyncClient, db_session: AsyncSession) -> None:
        concert = await create_concert(db_session)
        token = await _get_token(async_client)

        response = await async_client.delete(
            f"/api/v1/concerts/{concert.id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 204

    async def test_delete_returns_404_for_unknown(self, async_client: AsyncClient) -> None:
        token = await _get_token(async_client)
        response = await async_client.delete(
            "/api/v1/concerts/99999",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 404

    async def test_delete_requires_auth(self, async_client: AsyncClient, db_session: AsyncSession) -> None:
        concert = await create_concert(db_session)
        response = await async_client.delete(f"/api/v1/concerts/{concert.id}")
        assert response.status_code == 401
