"""Integration tests for health check and readiness endpoints."""

from __future__ import annotations

from collections.abc import AsyncGenerator

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


async def test_readiness_check_db_error_returns_degraded(async_client: AsyncClient) -> None:
    """When the DB connection fails, /ready must report status=degraded, not 5xx."""
    from app.db.session import get_db
    from app.main import app

    class _BrokenSession:
        async def execute(self, *_args: object, **_kwargs: object) -> None:
            raise RuntimeError("db connection lost")

    async def override_get_db() -> AsyncGenerator[_BrokenSession, None]:
        yield _BrokenSession()

    app.dependency_overrides[get_db] = override_get_db

    response = await async_client.get("/api/v1/ready")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "degraded"
    assert data["database"] == "error"


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


async def test_rate_limit_returns_429_after_threshold(async_client: AsyncClient) -> None:
    """Sending more than the allowed requests per window should return 429."""
    from app.main import _RATE_LIMIT_MAX, _rate_limit_store

    _rate_limit_store.clear()
    try:
        for _ in range(_RATE_LIMIT_MAX):
            response = await async_client.get("/api/v1/artists")
            assert response.status_code == 200

        response = await async_client.get("/api/v1/artists")
        assert response.status_code == 429
        assert response.json()["error"]["code"] == "RATE_LIMIT_EXCEEDED"
        assert "Retry-After" in response.headers
    finally:
        _rate_limit_store.clear()
