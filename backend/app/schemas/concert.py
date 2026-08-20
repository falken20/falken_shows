from __future__ import annotations

import math
from datetime import datetime
from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field

# ---------------------------------------------------------------------------
# Generic pagination wrapper
# ---------------------------------------------------------------------------

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated collection response."""

    items: list[T]
    total: int
    page: int
    page_size: int
    pages: int

    @classmethod
    def build(cls, items: list[T], total: int, page: int, page_size: int) -> PaginatedResponse[T]:
        pages = math.ceil(total / page_size) if page_size > 0 else 0
        return cls(items=items, total=total, page=page, page_size=page_size, pages=pages)


# ---------------------------------------------------------------------------
# Artist schemas
# ---------------------------------------------------------------------------


class ArtistBase(BaseModel):
    name: str = Field(..., max_length=255)
    bio: str | None = None
    country: str | None = Field(None, max_length=100)


class ArtistCreate(ArtistBase):
    pass


class ArtistUpdate(BaseModel):
    name: str | None = Field(None, max_length=255)
    bio: str | None = None
    country: str | None = Field(None, max_length=100)


class ArtistResponse(ArtistBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime


# ---------------------------------------------------------------------------
# Venue schemas
# ---------------------------------------------------------------------------


class VenueBase(BaseModel):
    name: str = Field(..., max_length=255)
    city: str = Field(..., max_length=100)
    country: str = Field(..., max_length=100)
    capacity: int | None = Field(None, ge=1)


class VenueCreate(VenueBase):
    pass


class VenueUpdate(BaseModel):
    name: str | None = Field(None, max_length=255)
    city: str | None = Field(None, max_length=100)
    country: str | None = Field(None, max_length=100)
    capacity: int | None = Field(None, ge=1)


class VenueResponse(VenueBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime


# ---------------------------------------------------------------------------
# Concert schemas
# ---------------------------------------------------------------------------


class ConcertBase(BaseModel):
    title: str = Field(..., max_length=255)
    artist_id: int | None = None
    venue_id: int | None = None
    date: datetime
    setlist: list[str] | None = None
    notes: str | None = None
    rating: int | None = Field(None, ge=1, le=5)
    ticket_price: float | None = Field(None, ge=0)
    currency: str = Field("EUR", max_length=3)


class ConcertCreate(ConcertBase):
    pass


class ConcertUpdate(BaseModel):
    title: str | None = Field(None, max_length=255)
    artist_id: int | None = None
    venue_id: int | None = None
    date: datetime | None = None
    setlist: list[str] | None = None
    notes: str | None = None
    rating: int | None = Field(None, ge=1, le=5)
    ticket_price: float | None = Field(None, ge=0)
    currency: str | None = Field(None, max_length=3)


class PhotoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    filename: str
    storage_url: str
    created_at: datetime


class ConcertResponse(ConcertBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    artist: ArtistResponse | None = None
    venue: VenueResponse | None = None
    photos: list[PhotoResponse] = []
    created_at: datetime
    updated_at: datetime
