"""auth lockout and token revocation tables

Revision ID: 002
Revises: 001
Create Date: 2026-09-15 00:00:00.000000
"""

from __future__ import annotations

import sqlalchemy as sa

from alembic import op

revision = "002"
down_revision = "001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "failed_login_attempts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("client_ip", sa.String(64), nullable=False),
        sa.Column(
            "attempted_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_failed_login_attempts_client_ip", "failed_login_attempts", ["client_ip"])
    op.create_index("ix_failed_login_attempts_attempted_at", "failed_login_attempts", ["attempted_at"])

    op.create_table(
        "revoked_tokens",
        sa.Column("jti", sa.String(36), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("jti"),
    )
    op.create_index("ix_revoked_tokens_expires_at", "revoked_tokens", ["expires_at"])


def downgrade() -> None:
    op.drop_index("ix_revoked_tokens_expires_at", table_name="revoked_tokens")
    op.drop_table("revoked_tokens")
    op.drop_index("ix_failed_login_attempts_attempted_at", table_name="failed_login_attempts")
    op.drop_index("ix_failed_login_attempts_client_ip", table_name="failed_login_attempts")
    op.drop_table("failed_login_attempts")
