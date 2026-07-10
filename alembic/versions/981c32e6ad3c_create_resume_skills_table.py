"""create_resume_skills_table

Revision ID: 981c32e6ad3c
Revises: 1a2070344173
Create Date: 2026-07-08

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# Revision identifiers.
revision: str = "981c32e6ad3c"
down_revision: Union[str, None] = "1a2070344173"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Create resume_skills table.
    """

    op.create_table(
        "resume_skills",

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
            "skill_name",
            sa.String(length=100),
            nullable=False,
        ),

        sa.Column(
            "category",
            sa.String(length=100),
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

        sa.UniqueConstraint(
            "resume_id",
            "skill_name",
            name="uq_resume_skill",
        ),
    )

    op.create_index(
        "ix_resume_skills_resume_id",
        "resume_skills",
        ["resume_id"],
    )

    op.create_index(
        "ix_resume_skills_skill_name",
        "resume_skills",
        ["skill_name"],
    )


def downgrade() -> None:
    """
    Drop resume_skills table.
    """

    op.drop_index(
        "ix_resume_skills_skill_name",
        table_name="resume_skills",
    )

    op.drop_index(
        "ix_resume_skills_resume_id",
        table_name="resume_skills",
    )

    op.drop_table("resume_skills")