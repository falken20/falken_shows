"""Test data factory functions for Live Memories test suite."""
from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.concert import Artist, Concert, Photo, Venue


async def create_artist(session: AsyncSession, **overrides: object) -> Artist:
    """Create and persist an Artist for testing."""
    data: dict[str, object] = {
        "name": "Test Artist",
        "bio": None,
        "country": "ES",
        **overrides,
    }
    artist = Artist(**data)  # type: ignore[arg-type]
    session.add(artist)
    await session.flush()
    await session.refresh(artist)
    return artist


async def create_venue(session: AsyncSession, **overrides: object) -> Venue:
    """Create and persist a Venue for testing."""
    data: dict[str, object] = {
        "name": "Test Venue",
        "city": "Madrid",
        "country": "ES",
        "capacity": None,
        **overrides,
    }
    venue = Venue(**data)  # type: ignore[arg-type]
    session.add(venue)
    await session.flush()
    await session.refresh(venue)
    return venue


async def create_concert(
    session: AsyncSession,
    *,
    artist: Artist | None = None,
    venue: Venue | None = None,
    **overrides: object,
) -> Concert:
    """Create and persist a Concert for testing."""
    data: dict[str, object] = {
        "title": "Test Concert",
        "artist_id": artist.id if artist else None,
        "venue_id": venue.id if venue else None,
        "date": datetime(2024, 6, 15, tzinfo=timezone.utc),
        "setlist": None,
        "notes": None,
        "rating": None,
        "ticket_price": None,
        "currency": "EUR",
        **overrides,
    }
    concert = Concert(**data)  # type: ignore[arg-type]
    session.add(concert)
    await session.flush()
    await session.refresh(concert)
    return concert


async def create_photo(
    session: AsyncSession,
    *,
    concert: Concert,
    **overrides: object,
) -> Photo:
    """Create and persist a Photo for testing."""
    data: dict[str, object] = {
        "concert_id": concert.id,
        "filename": "test.jpg",
        "storage_url": "https://example.com/test.jpg",
        **overrides,
    }
    photo = Photo(**data)  # type: ignore[arg-type]
    session.add(photo)
    await session.flush()
    await session.refresh(photo)
    return photo
