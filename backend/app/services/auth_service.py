from __future__ import annotations

import hmac

from app.core.exceptions import AppError, ErrorCode
from app.core.security import create_access_token, hash_password, verify_password
from app.core.config import settings


_ADMIN_PASSWORD_HASH = hash_password(settings.ADMIN_PASSWORD)


def authenticate(email: str, password: str) -> str:
    """Validate admin credentials and return a signed JWT.

    Raises:
        AppError: with ``ErrorCode.UNAUTHORIZED`` and HTTP 401 when the
            email or password is incorrect.
    """
    # Use constant-time comparison for identifiers used in auth checks.
    if not hmac.compare_digest(email, settings.ADMIN_EMAIL):
        raise AppError(ErrorCode.UNAUTHORIZED, status_code=401)

    if not verify_password(password, _ADMIN_PASSWORD_HASH):
        raise AppError(ErrorCode.UNAUTHORIZED, status_code=401)

    return create_access_token({"sub": email})
