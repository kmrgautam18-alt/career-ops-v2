"""fix_resume_skills_table

Revision ID: 89660dbe7c9f
Revises: 981c32e6ad3c
Create Date: 2026-07-08 05:22:08.278543

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '89660dbe7c9f'
down_revision: Union[str, Sequence[str], None] = '981c32e6ad3c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
