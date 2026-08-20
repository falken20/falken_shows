from __future__ import annotations

from collections.abc import AsyncGenerator

from sqlalchemy import Engine, create_engine
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


def _get_async_url() -> str:
    """Ensure DATABASE_URL uses the correct async driver prefix.

    - SQLite  → ``sqlite+aiosqlite://``
    - PostgreSQL → ``postgresql+asyncpg://``
    """
    url = settings.DATABASE_URL
    # Ensure proper async driver
    if "sqlite" in url and "+aiosqlite" not in url:
        url = url.replace("sqlite://", "sqlite+aiosqlite://", 1)
    if "postgresql" in url and "+asyncpg" not in url:
        url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
        url = url.replace("postgresql+psycopg2://", "postgresql+asyncpg://", 1)
    return url


def _get_sync_url() -> str:
    """Return a sync-driver URL for Alembic migrations and ``create_db_and_tables``.

    Strips async driver prefixes (aiosqlite, asyncpg) so Alembic's synchronous
    engine can connect without installing additional drivers.
    """
    url = settings.DATABASE_URL
    return url.replace("+aiosqlite", "").replace("+asyncpg", "+psycopg2")


def _build_async_engine() -> AsyncEngine:
    """Build the async SQLAlchemy engine from the current settings.

    SQLite connections receive ``check_same_thread=False`` so they can be used
    safely across threads in test environments.
    """
    async_url = _get_async_url()
    connect_args: dict[str, object] = {}
    if "sqlite" in async_url:
        connect_args["check_same_thread"] = False
    return create_async_engine(async_url, echo=settings.APP_DEBUG, connect_args=connect_args)


def _build_sync_engine() -> Engine:
    """Build a synchronous engine for DDL operations (create/drop tables).

    Not used at runtime – only called by ``create_db_and_tables`` during
    application startup in development and by test teardown.
    """
    sync_url = _get_sync_url()
    connect_args: dict[str, object] = {}
    if sync_url.startswith("sqlite"):
        connect_args["check_same_thread"] = False
    return create_engine(sync_url, echo=settings.APP_DEBUG, connect_args=connect_args)


async_engine: AsyncEngine = _build_async_engine()

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
    """Create all ORM tables that do not already exist.

    Uses a temporary synchronous engine so it can be called from the FastAPI
    ``lifespan`` context without requiring an active async event loop.  In
    production, prefer Alembic migrations (``make migrate``) over this helper.
    """
    sync_engine = _build_sync_engine()
    Base.metadata.create_all(bind=sync_engine)
    sync_engine.dispose()
