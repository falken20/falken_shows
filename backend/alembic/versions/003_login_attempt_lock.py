"""serialize login lockout updates

Revision ID: 003
Revises: 002
Create Date: 2026-09-21 00:00:00.000000
"""

from __future__ import annotations

import sqlalchemy as sa

from alembic import op

revision = "003"
down_revision = "002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "login_attempt_locks",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.execute(sa.text("INSERT INTO login_attempt_locks (id) VALUES (1)"))


def downgrade() -> None:
    op.drop_table("login_attempt_locks")
