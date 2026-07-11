from datetime import date
from datetime import datetime

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from backend.app.database.base import Base


class ResumeEducation(Base):
    """
    Structured education extracted from a resume.
    """

    __tablename__ = "resume_educations"

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

    degree: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        index=True,
    )

    specialization: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    institution: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    location: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    university: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    start_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    end_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    grade: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    percentage: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    cgpa: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    currently_studying: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default="false",
    )

    description: Mapped[str | None] = mapped_column(
        Text,
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
        back_populates="educations",
    )