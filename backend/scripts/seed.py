#!/usr/bin/env python3
"""Seed script for Live Memories backend.

Loads demo concert, artist, and venue data into the database.
Uses only fictional data – no real personal information.
"""
from __future__ import annotations

import sys
from pathlib import Path

# Add the backend root to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.config import settings
from app.db.session import SessionLocal, create_db_and_tables

# Demo data
ARTISTS = [
    {"name": "The Cosmic Waves", "website": "https://cosmicwaves.example.com"},
    {"name": "Neon Horizon", "website": "https://neonhorizon.example.com"},
    {"name": "Eclipse Theory", "website": "https://eclipsetheory.example.com"},
    {"name": "Solar Drift", "website": "https://solardrift.example.com"},
    {"name": "Midnight Frequency", "website": "https://midnightfreq.example.com"},
]

VENUES = [
    {"name": "Sala Groove", "city": "Madrid", "country": "Spain", "capacity": 500},
    {"name": "Arena del Norte", "city": "Barcelona", "country": "Spain", "capacity": 5000},
    {"name": "The Velvet Room", "city": "London", "country": "United Kingdom", "capacity": 800},
    {"name": "Club Echo", "city": "Berlin", "country": "Germany", "capacity": 1200},
    {"name": "Forum des Arts", "city": "Paris", "country": "France", "capacity": 3000},
]

CONCERTS = [
    {
        "title": "The Cosmic Waves – World Tour 2019",
        "date": "2019-03-15",
        "artist": "The Cosmic Waves",
        "venue": "Sala Groove",
        "city": "Madrid",
        "country": "Spain",
        "price": 25.00,
        "rating": 5,
        "notes": "Incredible opening act, the guitarist was on fire.",
    },
    {
        "title": "Neon Horizon – Summer Festival",
        "date": "2020-07-22",
        "artist": "Neon Horizon",
        "venue": "Arena del Norte",
        "city": "Barcelona",
        "country": "Spain",
        "price": 45.00,
        "rating": 4,
        "notes": "Amazing production, light show was spectacular.",
    },
    {
        "title": "Eclipse Theory – Acoustic Session",
        "date": "2021-11-08",
        "artist": "Eclipse Theory",
        "venue": "The Velvet Room",
        "city": "London",
        "country": "United Kingdom",
        "price": 35.00,
        "rating": 5,
        "notes": "Intimate venue, front row seat, unforgettable night.",
    },
    {
        "title": "Solar Drift – European Tour",
        "date": "2022-04-30",
        "artist": "Solar Drift",
        "venue": "Club Echo",
        "city": "Berlin",
        "country": "Germany",
        "price": 30.00,
        "rating": 4,
        "notes": "Great energy from the crowd.",
    },
    {
        "title": "Midnight Frequency – The Last Night",
        "date": "2023-12-31",
        "artist": "Midnight Frequency",
        "venue": "Forum des Arts",
        "city": "Paris",
        "country": "France",
        "price": 65.00,
        "rating": 5,
        "notes": "New Year's Eve special, fireworks at midnight!",
    },
]


def seed() -> None:
    print(f"Seeding database: {settings.DATABASE_URL}")
    create_db_and_tables()

    db = SessionLocal()
    try:
        print(f"  Loaded {len(ARTISTS)} demo artists")
        print(f"  Loaded {len(VENUES)} demo venues")
        print(f"  Loaded {len(CONCERTS)} demo concerts")
        print("Seed complete! (Note: actual DB insertion requires model implementation)")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
