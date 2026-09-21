"""Unit tests for database URL handling."""

from __future__ import annotations

from app.db import session as db_session


def test_injects_db_password_when_postgres_url_has_no_password(monkeypatch) -> None:
    monkeypatch.setattr(db_session.settings, "DB_PASSWORD", "secret-password")

    url = db_session._inject_db_password("postgresql+asyncpg://live_memories@/live_memories?host=/cloudsql/example")

    assert url.password == "secret-password"
    assert "secret-password" not in url.render_as_string(hide_password=True)


def test_keeps_existing_db_password(monkeypatch) -> None:
    monkeypatch.setattr(db_session.settings, "DB_PASSWORD", "ignored")

    raw = "postgresql+asyncpg://live_memories:existing@/live_memories?host=/cloudsql/example"
    url = db_session._inject_db_password(raw)

    assert url.password == "existing"
