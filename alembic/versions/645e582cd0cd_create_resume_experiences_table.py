"""create_resume_experiences_table

Revision ID: 645e582cd0cd
Revises: 89660dbe7c9f
Create Date: 2026-07-08 09:40:26.905996
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers
revision: str = "645e582cd0cd"
down_revision: str | Sequence[str] | None = "89660dbe7c9f"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "resume_experiences",

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
        ),

        sa.Column(
            "company",
            sa.String(length=255),
            nullable=True,
        ),

        sa.Column(
            "designation",
            sa.String(length=255),
            nullable=True,
        ),

        sa.Column(
            "employment_type",
            sa.String(length=100),
            nullable=True,
        ),

        sa.Column(
            "location",
            sa.String(length=255),
            nullable=True,
        ),

        sa.Column(
            "start_date",
            sa.Date(),
            nullable=True,
        ),

        sa.Column(
            "end_date",
            sa.Date(),
            nullable=True,
        ),

        sa.Column(
            "currently_working",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        ),

        sa.Column(
            "duration_months",
            sa.Integer(),
            nullable=True,
        ),

        sa.Column(
            "description",
            sa.Text(),
            nullable=True,
        ),

        sa.Column(
            "confidence",
            sa.Float(),
            nullable=False,
            server_default="1.0",
        ),

        sa.Column(
            "source",
            sa.String(length=50),
            nullable=False,
            server_default="knowledge_base",
        ),

        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.func.now(),
        ),
    )

    op.create_index(
        "ix_resume_experiences_resume_id",
        "resume_experiences",
        ["resume_id"],
    )

    op.create_index(
        "ix_resume_experiences_company",
        "resume_experiences",
        ["company"],
    )

    op.create_index(
        "ix_resume_experiences_designation",
        "resume_experiences",
        ["designation"],
    )


def downgrade() -> None:

    op.drop_index(
        "ix_resume_experiences_designation",
        table_name="resume_experiences",
    )

    op.drop_index(
        "ix_resume_experiences_company",
        table_name="resume_experiences",
    )

    op.drop_index(
        "ix_resume_experiences_resume_id",
        table_name="resume_experiences",
    )

    op.drop_table("resume_experiences")