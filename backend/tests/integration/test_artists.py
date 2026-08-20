"""Integration tests for the /api/v1/artists endpoints."""

from __future__ import annotations

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from tests.factories import create_artist

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


class TestListArtists:
    async def test_returns_empty_list_when_no_artists(self, async_client: AsyncClient) -> None:
        response = await async_client.get("/api/v1/artists")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0
        assert data["items"] == []

    async def test_returns_artists(self, async_client: AsyncClient, db_session: AsyncSession) -> None:
        await create_artist(db_session, name="Radiohead")
        await create_artist(db_session, name="Portishead")

        response = await async_client.get("/api/v1/artists")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 2
        names = {item["name"] for item in data["items"]}
        assert "Radiohead" in names
        assert "Portishead" in names

    async def test_pagination_params_are_respected(self, async_client: AsyncClient, db_session: AsyncSession) -> None:
        for i in range(5):
            await create_artist(db_session, name=f"Artist {i}")

        response = await async_client.get("/api/v1/artists?page=1&page_size=3")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 5
        assert len(data["items"]) == 3


class TestGetArtist:
    async def test_returns_artist(self, async_client: AsyncClient, db_session: AsyncSession) -> None:
        artist = await create_artist(db_session, name="Sigur Rós")
        response = await async_client.get(f"/api/v1/artists/{artist.id}")
        assert response.status_code == 200
        body = response.json()
        assert body["id"] == artist.id
        assert body["name"] == "Sigur Rós"

    async def test_returns_404_for_unknown_id(self, async_client: AsyncClient) -> None:
        response = await async_client.get("/api/v1/artists/99999")
        assert response.status_code == 404
        assert response.json()["error"]["code"] == "ARTIST_NOT_FOUND"


class TestCreateArtist:
    async def test_creates_artist_with_auth(self, async_client: AsyncClient) -> None:
        token = await _get_token(async_client)
        payload = {"name": "Nick Cave", "country": "AU"}
        response = await async_client.post(
            "/api/v1/artists",
            json=payload,
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 201
        body = response.json()
        assert body["name"] == "Nick Cave"
        assert body["country"] == "AU"
        assert "id" in body

    async def test_create_requires_auth(self, async_client: AsyncClient) -> None:
        response = await async_client.post("/api/v1/artists", json={"name": "Nick Cave"})
        assert response.status_code == 401

    async def test_create_validates_required_fields(self, async_client: AsyncClient) -> None:
        token = await _get_token(async_client)
        response = await async_client.post(
            "/api/v1/artists",
            json={},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 422


class TestUpdateArtist:
    async def test_updates_artist_with_auth(self, async_client: AsyncClient, db_session: AsyncSession) -> None:
        artist = await create_artist(db_session, name="Old Name")
        token = await _get_token(async_client)

        response = await async_client.put(
            f"/api/v1/artists/{artist.id}",
            json={"name": "New Name"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        assert response.json()["name"] == "New Name"

    async def test_update_returns_404_for_unknown(self, async_client: AsyncClient) -> None:
        token = await _get_token(async_client)
        response = await async_client.put(
            "/api/v1/artists/99999",
            json={"name": "New Name"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 404


class TestDeleteArtist:
    async def test_deletes_artist_with_auth(self, async_client: AsyncClient, db_session: AsyncSession) -> None:
        artist = await create_artist(db_session)
        token = await _get_token(async_client)

        response = await async_client.delete(
            f"/api/v1/artists/{artist.id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 204

    async def test_delete_returns_404_for_unknown(self, async_client: AsyncClient) -> None:
        token = await _get_token(async_client)
        response = await async_client.delete(
            "/api/v1/artists/99999",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 404

    async def test_delete_requires_auth(self, async_client: AsyncClient, db_session: AsyncSession) -> None:
        artist = await create_artist(db_session)
        response = await async_client.delete(f"/api/v1/artists/{artist.id}")
        assert response.status_code == 401
