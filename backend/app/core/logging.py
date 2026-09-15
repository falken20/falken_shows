from __future__ import annotations

import logging
import re
import sys

from app.core.config import settings

_SECRET_PATTERNS = (
    re.compile(r"(?i)(password|passwd|secret|token|authorization)\s*[=:]\s*\S+"),
    re.compile(r"(?i)(bearer\s+)[A-Za-z0-9._\-]+"),
)


def redact_secrets(message: str) -> str:
    """Mask credential-like values before they are written to logs."""
    redacted = message
    redacted = _SECRET_PATTERNS[0].sub(lambda m: f"{m.group(1)}=***", redacted)
    redacted = _SECRET_PATTERNS[1].sub(r"\1***", redacted)
    return redacted


class _RedactingFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        original = record.msg
        record.msg = redact_secrets(record.getMessage())
        record.args = ()
        try:
            return super().format(record)
        finally:
            record.msg = original


def configure_logging() -> None:
    """Configure the root logger for the application.

    In **production** (``APP_ENV=production``) every log line is emitted as a
    single-line JSON object compatible with Google Cloud Logging structured logs::

        {"timestamp": "...", "level": "INFO", "logger": "app.main", "message": "..."}

    In **development / testing** a human-readable format is used::

        2026-01-01 12:00:00 [INFO] app.main: startup ...

    Noisy third-party loggers (SQLAlchemy, Uvicorn access) are silenced to
    WARNING so they don't drown out application logs.
    """
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)

    formatter: logging.Formatter
    if settings.APP_ENV == "production":
        import json

        class JsonFormatter(logging.Formatter):
            def format(self, record: logging.LogRecord) -> str:
                log_entry = {
                    "timestamp": self.formatTime(record, "%Y-%m-%dT%H:%M:%S"),
                    "level": record.levelname,
                    "logger": record.name,
                    "message": redact_secrets(record.getMessage()),
                }
                if record.exc_info:
                    log_entry["exception"] = redact_secrets(self.formatException(record.exc_info))
                return json.dumps(log_entry)

        formatter = JsonFormatter()
    else:
        formatter = _RedactingFormatter(
            fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.handlers.clear()
    root_logger.addHandler(handler)

    # Quieten noisy libraries
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
