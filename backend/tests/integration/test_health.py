"""Integration tests for health check and readiness endpoints."""

from __future__ import annotations

from httpx import AsyncClient


async def test_health_check_returns_200(async_client: AsyncClient) -> None:
    response = await async_client.get("/api/v1/health")
    assert response.status_code == 200


async def test_health_check_response_body(async_client: AsyncClient) -> None:
    response = await async_client.get("/api/v1/health")
    data = response.json()
    assert data["status"] == "ok"
    assert "app_name" in data
    assert "version" in data
    assert "environment" in data


async def test_readiness_check_returns_200(async_client: AsyncClient) -> None:
    response = await async_client.get("/api/v1/ready")
    assert response.status_code == 200


async def test_readiness_check_db_ok(async_client: AsyncClient) -> None:
    response = await async_client.get("/api/v1/ready")
    data = response.json()
    assert data["status"] == "ok"
    assert data["database"] == "ok"


async def test_unknown_route_returns_404(async_client: AsyncClient) -> None:
    response = await async_client.get("/api/v1/does-not-exist")
    assert response.status_code == 404


async def test_security_headers_present(async_client: AsyncClient) -> None:
    response = await async_client.get("/api/v1/health")
    assert response.headers.get("x-content-type-options") == "nosniff"
    assert response.headers.get("x-frame-options") == "DENY"
    assert response.headers.get("referrer-policy") == "strict-origin-when-cross-origin"
    csp = "default-src 'none'; frame-ancestors 'none'; base-uri 'none'"
    assert response.headers.get("content-security-policy") == csp
    assert response.headers.get("permissions-policy") == "geolocation=(), camera=(), microphone=()"


async def test_request_id_header_present(async_client: AsyncClient) -> None:
    response = await async_client.get("/api/v1/health")
    assert "x-request-id" in response.headers
