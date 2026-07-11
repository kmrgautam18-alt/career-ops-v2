"""fix_resume_skills_table

Revision ID: 89660dbe7c9f
Revises: 981c32e6ad3c
Create Date: 2026-07-08 05:22:08.278543

"""
from collections.abc import Sequence

# revision identifiers, used by Alembic.
revision: str = '89660dbe7c9f'
down_revision: str | Sequence[str] | None = '981c32e6ad3c'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
