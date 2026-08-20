"""Unit tests for logging configuration."""

from __future__ import annotations

import json
import logging
import sys

import pytest

from app.core.config import settings
from app.core.logging import configure_logging


@pytest.fixture(autouse=True)
def _restore_logging() -> None:
    yield
    configure_logging()


def test_development_uses_human_readable_formatter(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(settings, "APP_ENV", "development")
    configure_logging()
    handler = logging.getLogger().handlers[0]
    record = logging.LogRecord("test", logging.INFO, __file__, 1, "hello", None, None)
    formatted = handler.formatter.format(record)  # type: ignore[union-attr]
    assert "hello" in formatted
    assert not formatted.strip().startswith("{")


def test_production_uses_json_formatter(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(settings, "APP_ENV", "production")
    configure_logging()
    handler = logging.getLogger().handlers[0]
    record = logging.LogRecord("test", logging.INFO, __file__, 1, "hello", None, None)
    formatted = handler.formatter.format(record)  # type: ignore[union-attr]
    payload = json.loads(formatted)
    assert payload["message"] == "hello"
    assert payload["level"] == "INFO"
    assert payload["logger"] == "test"


def test_production_json_formatter_includes_exception(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(settings, "APP_ENV", "production")
    configure_logging()
    handler = logging.getLogger().handlers[0]
    try:
        raise ValueError("boom")
    except ValueError:
        record = logging.LogRecord("test", logging.ERROR, __file__, 1, "failed", None, sys.exc_info())
    formatted = handler.formatter.format(record)  # type: ignore[union-attr]
    payload = json.loads(formatted)
    assert "boom" in payload["exception"]
