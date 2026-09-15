from __future__ import annotations

import hashlib
import hmac
from datetime import UTC, datetime, timedelta

from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.exceptions import AppError, ErrorCode
from app.core.security import create_access_token, hash_password, verify_password
from app.models.auth import FailedLoginAttempt, RevokedToken

_ADMIN_PASSWORD_HASH = hash_password(settings.ADMIN_PASSWORD)
_LOGIN_MAX_ATTEMPTS = 10
_LOGIN_WINDOW = 300
_MAX_PASSWORD_LENGTH = 128


def _digest(value: str) -> bytes:
    return hashlib.sha256(value.encode("utf-8")).digest()


async def authenticate(email: str, password: str, *, session: AsyncSession, client_ip: str = "unknown") -> str:
    """Validate admin credentials and return a signed JWT.

    Raises:
        AppError: with ``ErrorCode.UNAUTHORIZED`` and HTTP 401 when the
            email or password is incorrect.
        AppError: with ``ErrorCode.RATE_LIMIT_EXCEEDED`` after too many failures.
    """
    await _assert_login_allowed(session, client_ip)

    candidate = password if len(password) <= _MAX_PASSWORD_LENGTH else password[:_MAX_PASSWORD_LENGTH]
    email_ok = hmac.compare_digest(_digest(email), _digest(settings.ADMIN_EMAIL))
    password_ok = verify_password(candidate, _ADMIN_PASSWORD_HASH)
    if len(password) > _MAX_PASSWORD_LENGTH:
        password_ok = False

    if not (email_ok and password_ok):
        await _record_failed_login(session, client_ip)
        raise AppError(ErrorCode.UNAUTHORIZED, status_code=401)

    await _clear_failed_logins(session, client_ip)
    return create_access_token({"sub": settings.ADMIN_EMAIL})


async def revoke_access_token(session: AsyncSession, payload: dict[str, object]) -> None:
    """Persist the token ``jti`` so it cannot be reused until it expires."""
    jti = payload.get("jti")
    exp = payload.get("exp")
    if not isinstance(jti, str) or not isinstance(exp, (int, float)):
        raise AppError(ErrorCode.UNAUTHORIZED, status_code=401)
    expires_at = datetime.fromtimestamp(float(exp), tz=UTC)
    session.add(RevokedToken(jti=jti, expires_at=expires_at))
    await session.flush()


async def _assert_login_allowed(session: AsyncSession, client_ip: str) -> None:
    window_start = datetime.now(UTC) - timedelta(seconds=_LOGIN_WINDOW)
    await session.execute(delete(FailedLoginAttempt).where(FailedLoginAttempt.attempted_at < window_start))
    count = await session.scalar(
        select(func.count())
        .select_from(FailedLoginAttempt)
        .where(FailedLoginAttempt.client_ip == client_ip, FailedLoginAttempt.attempted_at > window_start)
    )
    if (count or 0) >= _LOGIN_MAX_ATTEMPTS:
        raise AppError(ErrorCode.RATE_LIMIT_EXCEEDED, status_code=429, message="Too many login attempts")


async def _record_failed_login(session: AsyncSession, client_ip: str) -> None:
    session.add(FailedLoginAttempt(client_ip=client_ip, attempted_at=datetime.now(UTC)))
    await session.commit()


async def _clear_failed_logins(session: AsyncSession, client_ip: str) -> None:
    await session.execute(delete(FailedLoginAttempt).where(FailedLoginAttempt.client_ip == client_ip))
    await session.flush()
