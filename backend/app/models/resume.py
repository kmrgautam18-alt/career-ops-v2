from datetime import datetime

from sqlalchemy import (
    DateTime,
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

from backend.app.core.resume_status import ResumeStatus
from backend.app.database.base import Base


class Resume(Base):
    """
    Resume metadata model.
    """

    __tablename__ = "resumes"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    original_filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    stored_filename: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )

    file_path: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    file_size: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    mime_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    upload_status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default=ResumeStatus.UPLOADED,
        server_default=ResumeStatus.UPLOADED,
    )

    # ==========================================
    # Resume Parsing Metadata
    # ==========================================

    parsed_text: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    parser_version: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    parsed_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # ==========================================
    # Relationships
    # ==========================================

    user = relationship(
        "User",
        back_populates="resumes",
    )

    profile = relationship(
        "ResumeProfile",
        back_populates="resume",
        uselist=False,
        cascade="all, delete-orphan",
    )

    skills = relationship(
        "ResumeSkill",
        back_populates="resume",
        cascade="all, delete-orphan",
    )
    experiences = relationship(
        "ResumeExperience",
        back_populates="resume",
        cascade="all, delete-orphan",
    )

    educations = relationship(
        "ResumeEducation",
        back_populates="resume",
        cascade="all, delete-orphan",
    )