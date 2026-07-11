"""create_resume_profiles_table

Revision ID: 1a2070344173
Revises: 284e62f63eb4
Create Date: 2026-07-07 18:07:25.975404
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "1a2070344173"
down_revision: str | Sequence[str] | None = "284e62f63eb4"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "resume_profiles",

        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True,
            autoincrement=True,
        ),

        sa.Column(
            "resume_id",
            sa.Integer(),
            sa.ForeignKey(
                "resumes.id",
                ondelete="CASCADE",
            ),
            nullable=False,
            unique=True,
        ),

        sa.Column(
            "full_name",
            sa.String(200),
            nullable=True,
        ),

        sa.Column(
            "email",
            sa.String(255),
            nullable=True,
        ),

        sa.Column(
            "phone",
            sa.String(50),
            nullable=True,
        ),

        sa.Column(
            "linkedin",
            sa.String(500),
            nullable=True,
        ),

        sa.Column(
            "github",
            sa.String(500),
            nullable=True,
        ),

        sa.Column(
            "portfolio",
            sa.String(500),
            nullable=True,
        ),

        sa.Column(
            "location",
            sa.String(255),
            nullable=True,
        ),

        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.func.now(),
            nullable=False,
        ),

        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_table("resume_profiles")