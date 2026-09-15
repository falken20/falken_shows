from __future__ import annotations

from fastapi import Request

from app.core.config import settings


def get_client_ip(request: Request) -> str:
    """Return the client IP for rate limiting and login lockout.

    When ``TRUST_PROXY_HEADERS`` is enabled the trusted reverse proxy is assumed
    to *append* to ``X-Forwarded-For``. The original client is then the
    second-to-last hop (the address that connected to our proxy). The leftmost
    value is ignored because clients can spoof it.
    """
    if settings.TRUST_PROXY_HEADERS:
        forwarded = request.headers.get("x-forwarded-for")
        if forwarded:
            parts = [part.strip() for part in forwarded.split(",") if part.strip()]
            if len(parts) >= 2:
                return parts[-2]
            if parts:
                return parts[-1]
    return request.client.host if request.client else "unknown"
