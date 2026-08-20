"""initial schema

Revision ID: 001
Revises:
Create Date: 2024-01-01 00:00:00.000000
"""
from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "artists",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("bio", sa.Text(), nullable=True),
        sa.Column("country", sa.String(100), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_artists_id", "artists", ["id"])
    op.create_index("ix_artists_name", "artists", ["name"])

    op.create_table(
        "venues",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("city", sa.String(100), nullable=False),
        sa.Column("country", sa.String(100), nullable=False),
        sa.Column("capacity", sa.Integer(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_venues_id", "venues", ["id"])
    op.create_index("ix_venues_name", "venues", ["name"])

    op.create_table(
        "concerts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("artist_id", sa.Integer(), nullable=True),
        sa.Column("venue_id", sa.Integer(), nullable=True),
        sa.Column("date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("setlist", sa.JSON(), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("rating", sa.Integer(), nullable=True),
        sa.Column("ticket_price", sa.Numeric(10, 2), nullable=True),
        sa.Column(
            "currency",
            sa.String(3),
            nullable=False,
            server_default="EUR",
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["artist_id"], ["artists.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["venue_id"], ["venues.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_concerts_id", "concerts", ["id"])
    op.create_index("ix_concerts_title", "concerts", ["title"])
    op.create_index("ix_concerts_artist_id", "concerts", ["artist_id"])
    op.create_index("ix_concerts_venue_id", "concerts", ["venue_id"])

    op.create_table(
        "photos",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("concert_id", sa.Integer(), nullable=False),
        sa.Column("filename", sa.String(255), nullable=False),
        sa.Column("storage_url", sa.Text(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["concert_id"], ["concerts.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_photos_id", "photos", ["id"])
    op.create_index("ix_photos_concert_id", "photos", ["concert_id"])


def downgrade() -> None:
    op.drop_index("ix_photos_concert_id", table_name="photos")
    op.drop_index("ix_photos_id", table_name="photos")
    op.drop_table("photos")

    op.drop_index("ix_concerts_venue_id", table_name="concerts")
    op.drop_index("ix_concerts_artist_id", table_name="concerts")
    op.drop_index("ix_concerts_title", table_name="concerts")
    op.drop_index("ix_concerts_id", table_name="concerts")
    op.drop_table("concerts")

    op.drop_index("ix_venues_name", table_name="venues")
    op.drop_index("ix_venues_id", table_name="venues")
    op.drop_table("venues")

    op.drop_index("ix_artists_name", table_name="artists")
    op.drop_index("ix_artists_id", table_name="artists")
    op.drop_table("artists")
