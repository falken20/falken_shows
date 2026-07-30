from __future__ import annotations

from collections.abc import Generator

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import settings


class Base(DeclarativeBase):
    pass


def _get_sync_url() -> str:
    """Convert async DB URL to sync URL."""
    url = settings.DATABASE_URL
    return url.replace("+aiosqlite", "").replace("+asyncpg", "+psycopg2")


def _build_engine() -> Engine:
    sync_url = _get_sync_url()
    connect_args: dict[str, object] = {}
    if sync_url.startswith("sqlite"):
        connect_args["check_same_thread"] = False
    return create_engine(sync_url, echo=settings.APP_DEBUG, connect_args=connect_args)


engine: Engine = _build_engine()

SessionLocal: sessionmaker[Session] = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def create_db_and_tables() -> None:
    """Create all tables if they don't exist. Used in development/testing."""
    Base.metadata.create_all(bind=engine)
