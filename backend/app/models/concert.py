from __future__ import annotations

from datetime import datetime

from sqlalchemy import JSON, DateTime, ForeignKey, Integer, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class Artist(Base):
    """A musical artist or band that performed at a concert."""

    __tablename__ = "artists"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)
    country: Mapped[str | None] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    concerts: Mapped[list[Concert]] = relationship("Concert", back_populates="artist")


class Venue(Base):
    """A physical location where concerts take place."""

    __tablename__ = "venues"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    country: Mapped[str] = mapped_column(String(100), nullable=False)
    capacity: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    concerts: Mapped[list[Concert]] = relationship("Concert", back_populates="venue")


class Concert(Base):
    """A concert experience logged in the personal inventory."""

    __tablename__ = "concerts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    artist_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("artists.id", ondelete="SET NULL"), nullable=True, index=True
    )
    venue_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("venues.id", ondelete="SET NULL"), nullable=True, index=True
    )
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    setlist: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    rating: Mapped[int | None] = mapped_column(Integer, nullable=True)
    ticket_price: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="EUR", server_default="EUR")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    artist: Mapped[Artist | None] = relationship("Artist", back_populates="concerts")
    venue: Mapped[Venue | None] = relationship("Venue", back_populates="concerts")
    photos: Mapped[list[Photo]] = relationship("Photo", back_populates="concert", cascade="all, delete-orphan")


class Photo(Base):
    """A photo attached to a concert."""

    __tablename__ = "photos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    concert_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("concerts.id", ondelete="CASCADE"), nullable=False, index=True
    )
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    storage_url: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    concert: Mapped[Concert] = relationship("Concert", back_populates="photos")
