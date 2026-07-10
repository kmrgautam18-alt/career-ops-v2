"""add_resume_parsing_fields

Revision ID: 284e62f63eb4
Revises: fb3db3a182e7
Create Date: 2026-07-07

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers
revision: str = "284e62f63eb4"
down_revision: Union[str, Sequence[str], None] = "fb3db3a182e7"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add resume parsing columns."""

    op.add_column(
        "resumes",
        sa.Column(
            "parsed_text",
            sa.Text(),
            nullable=True,
        ),
    )

    op.add_column(
        "resumes",
        sa.Column(
            "parser_version",
            sa.String(length=20),
            nullable=True,
        ),
    )

    op.add_column(
        "resumes",
        sa.Column(
            "parsed_at",
            sa.DateTime(),
            nullable=True,
        ),
    )


def downgrade() -> None:
    """Remove resume parsing columns."""

    op.drop_column("resumes", "parsed_at")
    op.drop_column("resumes", "parser_version")
    op.drop_column("resumes", "parsed_text")
