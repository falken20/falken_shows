from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AppError, ErrorCode
from app.repositories.concert_repository import ArtistRepository, ConcertRepository, VenueRepository
from app.schemas.concert import (
    ArtistCreate,
    ArtistResponse,
    ArtistUpdate,
    ConcertCreate,
    ConcertResponse,
    ConcertUpdate,
    PaginatedResponse,
    VenueCreate,
    VenueResponse,
    VenueUpdate,
)

_artist_repo = ArtistRepository()
_venue_repo = VenueRepository()
_concert_repo = ConcertRepository()


# ---------------------------------------------------------------------------
# Artist service
# ---------------------------------------------------------------------------


class ArtistService:
    async def list_artists(
        self, session: AsyncSession, page: int, page_size: int
    ) -> PaginatedResponse[ArtistResponse]:
        skip = (page - 1) * page_size
        artists, total = await _artist_repo.get_all(session, skip=skip, limit=page_size), await _artist_repo.count(session)
        items = [ArtistResponse.model_validate(a) for a in artists]
        return PaginatedResponse.build(items=items, total=total, page=page, page_size=page_size)

    async def get_artist(self, session: AsyncSession, artist_id: int) -> ArtistResponse:
        artist = await _artist_repo.get_by_id(session, artist_id)
        if artist is None:
            raise AppError(ErrorCode.ARTIST_NOT_FOUND, status_code=404)
        return ArtistResponse.model_validate(artist)

    async def create_artist(self, session: AsyncSession, data: ArtistCreate) -> ArtistResponse:
        artist = await _artist_repo.create(session, data)
        return ArtistResponse.model_validate(artist)

    async def update_artist(
        self, session: AsyncSession, artist_id: int, data: ArtistUpdate
    ) -> ArtistResponse:
        artist = await _artist_repo.get_by_id(session, artist_id)
        if artist is None:
            raise AppError(ErrorCode.ARTIST_NOT_FOUND, status_code=404)
        updated = await _artist_repo.update(session, artist, data)
        return ArtistResponse.model_validate(updated)

    async def delete_artist(self, session: AsyncSession, artist_id: int) -> None:
        artist = await _artist_repo.get_by_id(session, artist_id)
        if artist is None:
            raise AppError(ErrorCode.ARTIST_NOT_FOUND, status_code=404)
        await _artist_repo.delete(session, artist)


# ---------------------------------------------------------------------------
# Venue service
# ---------------------------------------------------------------------------


class VenueService:
    async def list_venues(
        self, session: AsyncSession, page: int, page_size: int
    ) -> PaginatedResponse[VenueResponse]:
        skip = (page - 1) * page_size
        venues, total = await _venue_repo.get_all(session, skip=skip, limit=page_size), await _venue_repo.count(session)
        items = [VenueResponse.model_validate(v) for v in venues]
        return PaginatedResponse.build(items=items, total=total, page=page, page_size=page_size)

    async def get_venue(self, session: AsyncSession, venue_id: int) -> VenueResponse:
        venue = await _venue_repo.get_by_id(session, venue_id)
        if venue is None:
            raise AppError(ErrorCode.VENUE_NOT_FOUND, status_code=404)
        return VenueResponse.model_validate(venue)

    async def create_venue(self, session: AsyncSession, data: VenueCreate) -> VenueResponse:
        venue = await _venue_repo.create(session, data)
        return VenueResponse.model_validate(venue)

    async def update_venue(
        self, session: AsyncSession, venue_id: int, data: VenueUpdate
    ) -> VenueResponse:
        venue = await _venue_repo.get_by_id(session, venue_id)
        if venue is None:
            raise AppError(ErrorCode.VENUE_NOT_FOUND, status_code=404)
        updated = await _venue_repo.update(session, venue, data)
        return VenueResponse.model_validate(updated)

    async def delete_venue(self, session: AsyncSession, venue_id: int) -> None:
        venue = await _venue_repo.get_by_id(session, venue_id)
        if venue is None:
            raise AppError(ErrorCode.VENUE_NOT_FOUND, status_code=404)
        await _venue_repo.delete(session, venue)


# ---------------------------------------------------------------------------
# Concert service
# ---------------------------------------------------------------------------


class ConcertService:
    async def list_concerts(
        self, session: AsyncSession, page: int, page_size: int
    ) -> PaginatedResponse[ConcertResponse]:
        skip = (page - 1) * page_size
        concerts, total = (
            await _concert_repo.get_all(session, skip=skip, limit=page_size),
            await _concert_repo.count(session),
        )
        items = [ConcertResponse.model_validate(c) for c in concerts]
        return PaginatedResponse.build(items=items, total=total, page=page, page_size=page_size)

    async def get_concert(self, session: AsyncSession, concert_id: int) -> ConcertResponse:
        concert = await _concert_repo.get_by_id(session, concert_id)
        if concert is None:
            raise AppError(ErrorCode.CONCERT_NOT_FOUND, status_code=404)
        return ConcertResponse.model_validate(concert)

    async def create_concert(self, session: AsyncSession, data: ConcertCreate) -> ConcertResponse:
        concert = await _concert_repo.create(session, data)
        return ConcertResponse.model_validate(concert)

    async def update_concert(
        self, session: AsyncSession, concert_id: int, data: ConcertUpdate
    ) -> ConcertResponse:
        concert = await _concert_repo.get_by_id(session, concert_id)
        if concert is None:
            raise AppError(ErrorCode.CONCERT_NOT_FOUND, status_code=404)
        updated = await _concert_repo.update(session, concert, data)
        return ConcertResponse.model_validate(updated)

    async def delete_concert(self, session: AsyncSession, concert_id: int) -> None:
        concert = await _concert_repo.get_by_id(session, concert_id)
        if concert is None:
            raise AppError(ErrorCode.CONCERT_NOT_FOUND, status_code=404)
        await _concert_repo.delete(session, concert)
