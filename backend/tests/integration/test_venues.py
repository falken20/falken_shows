"""Integration tests for the /api/v1/venues endpoints."""

from __future__ import annotations

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from tests.factories import create_venue

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


class TestListVenues:
    async def test_returns_empty_list_when_no_venues(self, async_client: AsyncClient) -> None:
        response = await async_client.get("/api/v1/venues")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0
        assert data["items"] == []

    async def test_returns_venues(self, async_client: AsyncClient, db_session: AsyncSession) -> None:
        await create_venue(db_session, name="Wembley Arena", city="London", country="GB")
        await create_venue(db_session, name="Palau Sant Jordi", city="Barcelona", country="ES")

        response = await async_client.get("/api/v1/venues")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 2
        names = {item["name"] for item in data["items"]}
        assert "Wembley Arena" in names
        assert "Palau Sant Jordi" in names

    async def test_pagination_params_are_respected(self, async_client: AsyncClient, db_session: AsyncSession) -> None:
        for i in range(5):
            await create_venue(db_session, name=f"Venue {i}")

        response = await async_client.get("/api/v1/venues?page=1&page_size=3")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 5
        assert len(data["items"]) == 3


class TestGetVenue:
    async def test_returns_venue(self, async_client: AsyncClient, db_session: AsyncSession) -> None:
        venue = await create_venue(db_session, name="Red Rocks", capacity=9525)
        response = await async_client.get(f"/api/v1/venues/{venue.id}")
        assert response.status_code == 200
        body = response.json()
        assert body["id"] == venue.id
        assert body["name"] == "Red Rocks"
        assert body["capacity"] == 9525

    async def test_returns_404_for_unknown_id(self, async_client: AsyncClient) -> None:
        response = await async_client.get("/api/v1/venues/99999")
        assert response.status_code == 404
        assert response.json()["error"]["code"] == "VENUE_NOT_FOUND"


class TestCreateVenue:
    async def test_creates_venue_with_auth(self, async_client: AsyncClient) -> None:
        token = await _get_token(async_client)
        payload = {"name": "The O2", "city": "London", "country": "GB", "capacity": 20000}
        response = await async_client.post(
            "/api/v1/venues",
            json=payload,
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 201
        body = response.json()
        assert body["name"] == "The O2"
        assert body["capacity"] == 20000
        assert "id" in body

    async def test_create_requires_auth(self, async_client: AsyncClient) -> None:
        payload = {"name": "The O2", "city": "London", "country": "GB"}
        response = await async_client.post("/api/v1/venues", json=payload)
        assert response.status_code == 401

    async def test_create_validates_required_fields(self, async_client: AsyncClient) -> None:
        token = await _get_token(async_client)
        response = await async_client.post(
            "/api/v1/venues",
            json={},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 422


class TestUpdateVenue:
    async def test_updates_venue_with_auth(self, async_client: AsyncClient, db_session: AsyncSession) -> None:
        venue = await create_venue(db_session, name="Old Name")
        token = await _get_token(async_client)

        response = await async_client.put(
            f"/api/v1/venues/{venue.id}",
            json={"name": "New Name"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        assert response.json()["name"] == "New Name"

    async def test_update_returns_404_for_unknown(self, async_client: AsyncClient) -> None:
        token = await _get_token(async_client)
        response = await async_client.put(
            "/api/v1/venues/99999",
            json={"name": "New Name"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 404


class TestDeleteVenue:
    async def test_deletes_venue_with_auth(self, async_client: AsyncClient, db_session: AsyncSession) -> None:
        venue = await create_venue(db_session)
        token = await _get_token(async_client)

        response = await async_client.delete(
            f"/api/v1/venues/{venue.id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 204

    async def test_delete_returns_404_for_unknown(self, async_client: AsyncClient) -> None:
        token = await _get_token(async_client)
        response = await async_client.delete(
            "/api/v1/venues/99999",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 404

    async def test_delete_requires_auth(self, async_client: AsyncClient, db_session: AsyncSession) -> None:
        venue = await create_venue(db_session)
        response = await async_client.delete(f"/api/v1/venues/{venue.id}")
        assert response.status_code == 401
