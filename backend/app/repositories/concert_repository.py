from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.concert import Artist, Concert, Photo, Venue
from app.schemas.concert import (
    ArtistCreate,
    ArtistUpdate,
    ConcertCreate,
    ConcertUpdate,
    VenueCreate,
    VenueUpdate,
)


# ---------------------------------------------------------------------------
# Artist repository
# ---------------------------------------------------------------------------


class ArtistRepository:
    async def get_all(self, session: AsyncSession, *, skip: int, limit: int) -> list[Artist]:
        result = await session.execute(
            select(Artist).order_by(Artist.id).offset(skip).limit(limit)
        )
        return list(result.scalars().all())

    async def count(self, session: AsyncSession) -> int:
        result = await session.execute(select(func.count()).select_from(Artist))
        return result.scalar_one()

    async def get_by_id(self, session: AsyncSession, artist_id: int) -> Artist | None:
        result = await session.execute(select(Artist).where(Artist.id == artist_id))
        return result.scalar_one_or_none()

    async def create(self, session: AsyncSession, data: ArtistCreate) -> Artist:
        artist = Artist(**data.model_dump())
        session.add(artist)
        await session.flush()
        await session.refresh(artist)
        return artist

    async def update(self, session: AsyncSession, artist: Artist, data: ArtistUpdate) -> Artist:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(artist, field, value)
        await session.flush()
        await session.refresh(artist)
        return artist

    async def delete(self, session: AsyncSession, artist: Artist) -> None:
        await session.delete(artist)
        await session.flush()


# ---------------------------------------------------------------------------
# Venue repository
# ---------------------------------------------------------------------------


class VenueRepository:
    async def get_all(self, session: AsyncSession, *, skip: int, limit: int) -> list[Venue]:
        result = await session.execute(
            select(Venue).order_by(Venue.id).offset(skip).limit(limit)
        )
        return list(result.scalars().all())

    async def count(self, session: AsyncSession) -> int:
        result = await session.execute(select(func.count()).select_from(Venue))
        return result.scalar_one()

    async def get_by_id(self, session: AsyncSession, venue_id: int) -> Venue | None:
        result = await session.execute(select(Venue).where(Venue.id == venue_id))
        return result.scalar_one_or_none()

    async def create(self, session: AsyncSession, data: VenueCreate) -> Venue:
        venue = Venue(**data.model_dump())
        session.add(venue)
        await session.flush()
        await session.refresh(venue)
        return venue

    async def update(self, session: AsyncSession, venue: Venue, data: VenueUpdate) -> Venue:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(venue, field, value)
        await session.flush()
        await session.refresh(venue)
        return venue

    async def delete(self, session: AsyncSession, venue: Venue) -> None:
        await session.delete(venue)
        await session.flush()


# ---------------------------------------------------------------------------
# Concert repository
# ---------------------------------------------------------------------------

_CONCERT_EAGER = [
    selectinload(Concert.artist),
    selectinload(Concert.venue),
    selectinload(Concert.photos),
]


class ConcertRepository:
    async def get_all(self, session: AsyncSession, *, skip: int, limit: int) -> list[Concert]:
        result = await session.execute(
            select(Concert)
            .options(*_CONCERT_EAGER)
            .order_by(Concert.date.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def count(self, session: AsyncSession) -> int:
        result = await session.execute(select(func.count()).select_from(Concert))
        return result.scalar_one()

    async def get_by_id(self, session: AsyncSession, concert_id: int) -> Concert | None:
        result = await session.execute(
            select(Concert).options(*_CONCERT_EAGER).where(Concert.id == concert_id)
        )
        return result.scalar_one_or_none()

    async def create(self, session: AsyncSession, data: ConcertCreate) -> Concert:
        concert = Concert(**data.model_dump())
        session.add(concert)
        await session.flush()
        # Re-fetch with relationships
        refreshed = await self.get_by_id(session, concert.id)
        assert refreshed is not None  # noqa: S101 – just flushed
        return refreshed

    async def update(self, session: AsyncSession, concert: Concert, data: ConcertUpdate) -> Concert:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(concert, field, value)
        await session.flush()
        refreshed = await self.get_by_id(session, concert.id)
        assert refreshed is not None  # noqa: S101 – just flushed
        return refreshed

    async def delete(self, session: AsyncSession, concert: Concert) -> None:
        await session.delete(concert)
        await session.flush()


# ---------------------------------------------------------------------------
# Photo repository (thin – photos are uploaded via a separate flow)
# ---------------------------------------------------------------------------


class PhotoRepository:
    async def get_by_id(self, session: AsyncSession, photo_id: int) -> Photo | None:
        result = await session.execute(select(Photo).where(Photo.id == photo_id))
        return result.scalar_one_or_none()

    async def delete(self, session: AsyncSession, photo: Photo) -> None:
        await session.delete(photo)
        await session.flush()
