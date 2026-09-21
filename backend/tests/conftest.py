"""Shared pytest fixtures for Live Memories backend tests."""

from __future__ import annotations

import os
from collections.abc import AsyncGenerator

os.environ["APP_ENV"] = "testing"

import pytest  # noqa: E402
from httpx import ASGITransport, AsyncClient  # noqa: E402
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine  # noqa: E402

from app.db.session import Base, _enable_sqlite_fk, get_db  # noqa: E402
from app.main import app  # noqa: E402

# ── In-memory SQLite for tests ────────────────────────────────
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    test_engine = create_async_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    _enable_sqlite_fk(test_engine.sync_engine)
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    TestSessionLocal = async_sessionmaker(bind=test_engine, expire_on_commit=False)
    async with TestSessionLocal() as session:
        yield session
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await test_engine.dispose()


@pytest.fixture(scope="function")
async def async_client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture()
async def auth_token(async_client: AsyncClient) -> str:
    """Obtain a valid JWT for the default admin user."""
    response = await async_client.post(
        "/api/v1/auth/token",
        data={"username": "admin@example.com", "password": "change-me-in-production"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200
    return str(response.json()["access_token"])


@pytest.fixture()
def auth_headers(auth_token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {auth_token}"}
