from __future__ import annotations

from typing import Annotated, Any

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_current_user
from app.db.session import get_db
from app.schemas.concert import ConcertCreate, ConcertResponse, ConcertUpdate, PaginatedResponse
from app.services.concert_service import ConcertService

router = APIRouter()
_service = ConcertService()


@router.get("", response_model=PaginatedResponse[ConcertResponse])
async def list_concerts(
    db: Annotated[AsyncSession, Depends(get_db)],
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
) -> PaginatedResponse[ConcertResponse]:
    """List all concerts (public – no auth required)."""
    return await _service.list_concerts(db, page=page, page_size=page_size)


@router.post("", response_model=ConcertResponse, status_code=status.HTTP_201_CREATED)
async def create_concert(
    data: ConcertCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _user: Annotated[dict[str, Any], Depends(get_current_user)],
) -> ConcertResponse:
    """Create a new concert entry. Requires authentication."""
    return await _service.create_concert(db, data)


@router.get("/{concert_id}", response_model=ConcertResponse)
async def get_concert(
    concert_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ConcertResponse:
    """Retrieve a single concert by ID (public)."""
    return await _service.get_concert(db, concert_id)


@router.put("/{concert_id}", response_model=ConcertResponse)
async def update_concert(
    concert_id: int,
    data: ConcertUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _user: Annotated[dict[str, Any], Depends(get_current_user)],
) -> ConcertResponse:
    """Update a concert entry. Requires authentication."""
    return await _service.update_concert(db, concert_id, data)


@router.delete("/{concert_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
async def delete_concert(
    concert_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    _user: Annotated[dict[str, Any], Depends(get_current_user)],
) -> None:
    """Delete a concert entry. Requires authentication."""
    await _service.delete_concert(db, concert_id)
