from __future__ import annotations

from typing import Annotated, Any

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_current_user
from app.db.session import get_db
from app.schemas.concert import ArtistCreate, ArtistResponse, ArtistUpdate, PaginatedResponse
from app.services.concert_service import ArtistService

router = APIRouter()
_service = ArtistService()


@router.get("", response_model=PaginatedResponse[ArtistResponse])
async def list_artists(
    db: Annotated[AsyncSession, Depends(get_db)],
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
) -> PaginatedResponse[ArtistResponse]:
    """List all artists (public)."""
    return await _service.list_artists(db, page=page, page_size=page_size)


@router.post("", response_model=ArtistResponse, status_code=status.HTTP_201_CREATED)
async def create_artist(
    data: ArtistCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _user: Annotated[dict[str, Any], Depends(get_current_user)],
) -> ArtistResponse:
    """Create a new artist. Requires authentication."""
    return await _service.create_artist(db, data)


@router.get("/{artist_id}", response_model=ArtistResponse)
async def get_artist(
    artist_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ArtistResponse:
    """Retrieve a single artist by ID (public)."""
    return await _service.get_artist(db, artist_id)


@router.put("/{artist_id}", response_model=ArtistResponse)
async def update_artist(
    artist_id: int,
    data: ArtistUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _user: Annotated[dict[str, Any], Depends(get_current_user)],
) -> ArtistResponse:
    """Update an artist. Requires authentication."""
    return await _service.update_artist(db, artist_id, data)


@router.delete("/{artist_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
async def delete_artist(
    artist_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    _user: Annotated[dict[str, Any], Depends(get_current_user)],
) -> None:
    """Delete an artist. Requires authentication."""
    await _service.delete_artist(db, artist_id)
