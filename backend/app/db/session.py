from __future__ import annotations

from collections.abc import AsyncGenerator

from sqlalchemy import Engine, create_engine, event
from sqlalchemy.engine import URL, make_url
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


class Base(DeclarativeBase):
    """Shared SQLAlchemy declarative base for all ORM models.

    Import this class in every model module and inherit from it::

        from app.db.session import Base

        class Concert(Base):
            __tablename__ = "concerts"
            ...
    """


def _inject_db_password(url: str) -> URL:
    """Return a SQLAlchemy URL, injecting ``DB_PASSWORD`` when PostgreSQL has none.

    The URL object is passed to the engine so the password is not rendered into
    a loggable connection string.
    """
    parsed = make_url(url)
    if "postgresql" not in url or settings.DB_PASSWORD is None:
        return parsed
    if parsed.password is not None:
        return parsed
    return parsed.set(password=settings.DB_PASSWORD)


def _get_async_url() -> URL:
    """Ensure DATABASE_URL uses the correct async driver prefix.

    - SQLite  → ``sqlite+aiosqlite://``
    - PostgreSQL → ``postgresql+asyncpg://``
    """
    parsed = _inject_db_password(settings.DATABASE_URL)
    driver = parsed.drivername
    if "sqlite" in driver and "+aiosqlite" not in driver:
        parsed = parsed.set(drivername="sqlite+aiosqlite")
    if "postgresql" in driver and "+asyncpg" not in driver:
        parsed = parsed.set(drivername="postgresql+asyncpg")
    return parsed


def _get_sync_url() -> URL:
    """Return a sync-driver URL for Alembic migrations and ``create_db_and_tables``."""
    parsed = _inject_db_password(settings.DATABASE_URL)
    driver = parsed.drivername.replace("+aiosqlite", "").replace("+asyncpg", "+psycopg2")
    if driver == "postgresql":
        driver = "postgresql+psycopg2"
    return parsed.set(drivername=driver)


def _enable_sqlite_fk(engine: Engine) -> None:
    """Enable FK constraint enforcement for SQLite connections."""
    if "sqlite" in str(engine.url):
        event.listen(engine, "connect", lambda conn, _rec: conn.execute("PRAGMA foreign_keys=ON"))


def _build_async_engine() -> AsyncEngine:
    """Build the async SQLAlchemy engine from the current settings.

    SQLite connections receive ``check_same_thread=False`` so they can be used
    safely across threads in test environments.
    """
    async_url = _get_async_url()
    connect_args: dict[str, object] = {}
    if "sqlite" in async_url.drivername:
        connect_args["check_same_thread"] = False
    return create_async_engine(async_url, echo=settings.sql_echo, connect_args=connect_args)


def _build_sync_engine() -> Engine:
    """Build a synchronous engine for DDL operations (create/drop tables)."""
    sync_url = _get_sync_url()
    connect_args: dict[str, object] = {}
    if sync_url.drivername.startswith("sqlite"):
        connect_args["check_same_thread"] = False
    return create_engine(sync_url, echo=settings.sql_echo, connect_args=connect_args)


async_engine: AsyncEngine = _build_async_engine()
_enable_sqlite_fk(async_engine.sync_engine)

AsyncSessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency that yields a transactional ``AsyncSession``.

    Commits on success and rolls back on any exception, then closes the
    session.  Use with ``Depends``::

        from typing import Annotated
        from fastapi import Depends
        from sqlalchemy.ext.asyncio import AsyncSession
        from app.db.session import get_db

        async def my_endpoint(db: Annotated[AsyncSession, Depends(get_db)]) -> ...
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


def create_db_and_tables() -> None:
    """Create all ORM tables that do not already exist."""
    sync_engine = _build_sync_engine()
    _enable_sqlite_fk(sync_engine)
    Base.metadata.create_all(bind=sync_engine)
    sync_engine.dispose()
