from __future__ import annotations

from fastapi import Request


def get_client_ip(request: Request) -> str:
    """Return the client IP for rate limiting and login lockout.

    ``X-Forwarded-For`` is not used here because its contents can be supplied
    by the client before a proxy appends its own value. Using it for security
    controls would let a client select a new rate-limit key on every request.
    Deployments that need per-client limits behind a proxy must sanitize the
    header at the trusted edge before exposing that identity to the app.
    """
    return request.client.host if request.client else "unknown"
