from datetime import datetime

from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from backend.app.database.base import Base


class ResumeSkill(Base):
    """
    Normalized skill extracted from a resume.

    This model is intentionally future-ready for the
    Universal Career Intelligence Engine.

    Current extractor fills only a subset of fields.
    AI-based extractors will populate the remaining
    metadata in future versions.
    """

    __tablename__ = "resume_skills"

    __table_args__ = (
        UniqueConstraint(
            "resume_id",
            "skill_name",
            name="uq_resume_skill",
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    resume_id: Mapped[int] = mapped_column(
        ForeignKey(
            "resumes.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    skill_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    category: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    confidence: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=1.0,
        server_default="1.0",
    )

    source: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="knowledge_base",
        server_default="knowledge_base",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )

    resume = relationship(
        "Resume",
        back_populates="skills",
    )