#!/usr/bin/env python3
"""Seed script for Live Memories backend.

Loads demo concert, artist, and venue data into the database.
Uses only fictional data – no real personal information.
"""

from __future__ import annotations

import asyncio
import sys
from datetime import UTC, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.db.session import AsyncSessionLocal, Base, _build_sync_engine  # noqa: E402
from app.models.concert import Artist, Concert, Venue  # noqa: E402

ARTISTS = [
    {"name": "The Cosmic Waves", "bio": "Space-rock band from Madrid", "country": "ES"},
    {"name": "Neon Horizon", "bio": "Electronic duo from Barcelona", "country": "ES"},
    {"name": "Eclipse Theory", "bio": "Post-rock from London", "country": "GB"},
    {"name": "Solar Drift", "bio": "Ambient from Berlin", "country": "DE"},
    {"name": "Midnight Frequency", "bio": "Synthwave from Paris", "country": "FR"},
]

VENUES = [
    {"name": "Sala Groove", "city": "Madrid", "country": "ES", "capacity": 500},
    {"name": "Arena del Norte", "city": "Barcelona", "country": "ES", "capacity": 5000},
    {"name": "The Velvet Room", "city": "London", "country": "GB", "capacity": 800},
    {"name": "Club Echo", "city": "Berlin", "country": "DE", "capacity": 1200},
    {"name": "Forum des Arts", "city": "Paris", "country": "FR", "capacity": 3000},
]

CONCERTS = [
    {
        "title": "Cosmic Waves - World Tour 2019",
        "artist_idx": 0,
        "venue_idx": 0,
        "date": "2019-03-15",
        "ticket_price": 25.00,
        "rating": 5,
        "notes": "Incredible opening act.",
    },
    {
        "title": "Neon Horizon - Summer Festival",
        "artist_idx": 1,
        "venue_idx": 1,
        "date": "2020-07-22",
        "ticket_price": 45.00,
        "rating": 4,
        "notes": "Amazing light show.",
    },
    {
        "title": "Eclipse Theory - Acoustic Session",
        "artist_idx": 2,
        "venue_idx": 2,
        "date": "2021-11-08",
        "ticket_price": 35.00,
        "rating": 5,
        "notes": "Front row seat.",
    },
    {
        "title": "Solar Drift - European Tour",
        "artist_idx": 3,
        "venue_idx": 3,
        "date": "2022-04-30",
        "ticket_price": 30.00,
        "rating": 4,
        "notes": "Great energy.",
    },
    {
        "title": "Midnight Frequency - NYE",
        "artist_idx": 4,
        "venue_idx": 4,
        "date": "2023-12-31",
        "ticket_price": 65.00,
        "rating": 5,
        "notes": "Fireworks at midnight!",
    },
]


async def seed() -> None:
    sync_engine = _build_sync_engine()
    Base.metadata.create_all(bind=sync_engine)
    sync_engine.dispose()

    async with AsyncSessionLocal() as session:
        artists: list[Artist] = []
        for data in ARTISTS:
            a = Artist(**data)
            session.add(a)
            artists.append(a)
        await session.flush()

        venues: list[Venue] = []
        for data in VENUES:
            v = Venue(**data)
            session.add(v)
            venues.append(v)
        await session.flush()

        for data in CONCERTS:
            c = Concert(
                title=data["title"],
                artist_id=artists[data["artist_idx"]].id,
                venue_id=venues[data["venue_idx"]].id,
                date=datetime.strptime(data["date"], "%Y-%m-%d").replace(tzinfo=UTC),
                ticket_price=data["ticket_price"],
                rating=data["rating"],
                notes=data["notes"],
                currency="EUR",
            )
            session.add(c)

        await session.commit()
        print(f"Seeded {len(ARTISTS)} artists, {len(VENUES)} venues, {len(CONCERTS)} concerts.")


if __name__ == "__main__":
    asyncio.run(seed())
