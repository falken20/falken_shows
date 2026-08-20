from __future__ import annotations

from typing import Annotated, Any

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_current_user
from app.db.session import get_db
from app.schemas.concert import PaginatedResponse, VenueCreate, VenueResponse, VenueUpdate
from app.services.concert_service import VenueService

router = APIRouter()
_service = VenueService()


@router.get("", response_model=PaginatedResponse[VenueResponse])
async def list_venues(
    db: Annotated[AsyncSession, Depends(get_db)],
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
) -> PaginatedResponse[VenueResponse]:
    """List all venues (public)."""
    return await _service.list_venues(db, page=page, page_size=page_size)


@router.post("", response_model=VenueResponse, status_code=status.HTTP_201_CREATED)
async def create_venue(
    data: VenueCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _user: Annotated[dict[str, Any], Depends(get_current_user)],
) -> VenueResponse:
    """Create a new venue. Requires authentication."""
    return await _service.create_venue(db, data)


@router.get("/{venue_id}", response_model=VenueResponse)
async def get_venue(
    venue_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> VenueResponse:
    """Retrieve a single venue by ID (public)."""
    return await _service.get_venue(db, venue_id)


@router.put("/{venue_id}", response_model=VenueResponse)
async def update_venue(
    venue_id: int,
    data: VenueUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _user: Annotated[dict[str, Any], Depends(get_current_user)],
) -> VenueResponse:
    """Update a venue. Requires authentication."""
    return await _service.update_venue(db, venue_id, data)


@router.delete("/{venue_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
async def delete_venue(
    venue_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    _user: Annotated[dict[str, Any], Depends(get_current_user)],
) -> None:
    """Delete a venue. Requires authentication."""
    await _service.delete_venue(db, venue_id)
