from __future__ import annotations

import hmac
import time
from collections import defaultdict

from app.core.config import settings
from app.core.exceptions import AppError, ErrorCode
from app.core.security import create_access_token, hash_password, verify_password

_ADMIN_PASSWORD_HASH = hash_password(settings.ADMIN_PASSWORD)
_failed_login_attempts: dict[str, list[float]] = defaultdict(list)
_LOGIN_MAX_ATTEMPTS = 10
_LOGIN_WINDOW = 300


def authenticate(email: str, password: str, *, client_ip: str = "unknown") -> str:
    """Validate admin credentials and return a signed JWT.

    Raises:
        AppError: with ``ErrorCode.UNAUTHORIZED`` and HTTP 401 when the
            email or password is incorrect.
    """
    _assert_login_allowed(client_ip)

    if not hmac.compare_digest(email, settings.ADMIN_EMAIL) or not verify_password(password, _ADMIN_PASSWORD_HASH):
        _record_failed_login(client_ip)
        raise AppError(ErrorCode.UNAUTHORIZED, status_code=401)

    _failed_login_attempts.pop(client_ip, None)
    return create_access_token({"sub": email})


def _assert_login_allowed(client_ip: str) -> None:
    now = time.time()
    window_start = now - _LOGIN_WINDOW
    _failed_login_attempts[client_ip] = [t for t in _failed_login_attempts[client_ip] if t > window_start]
    if len(_failed_login_attempts[client_ip]) >= _LOGIN_MAX_ATTEMPTS:
        raise AppError(ErrorCode.RATE_LIMIT_EXCEEDED, status_code=429, message="Too many login attempts")


def _record_failed_login(client_ip: str) -> None:
    _failed_login_attempts[client_ip].append(time.time())
