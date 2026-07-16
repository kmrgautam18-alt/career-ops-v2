"""
Auto Job Application Engine — Database Models
Tracks sourced jobs, AI-optimized resumes, email applications, interviews, and follow-ups.
"""

from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.database.base import Base


class AutoApplication(Base):
    """
    Tracks a job sourced from a portal, AI-optimized, and auto-applied.
    Includes interview tracking and follow-up scheduling.
    """

    __tablename__ = "auto_applications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    job_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("jobs.id", ondelete="SET NULL"), nullable=True
    )

    # Job sourcing
    source: Mapped[str] = mapped_column(
        String(50), nullable=False, default="manual"
    )  # linkedin, indeed, company_career, google_jobs, manual
    source_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    company: Mapped[str] = mapped_column(String(200), nullable=False)
    job_title: Mapped[str] = mapped_column(String(200), nullable=False)
    job_description: Mapped[str | None] = mapped_column(Text, nullable=True)
    company_email: Mapped[str | None] = mapped_column(
        String(255), nullable=True
    )  # HR email

    # AI processing
    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="sourced",
        server_default="sourced",
    )
    # Status flow: sourced → ai_optimized → emailed → interview_scheduled
    #              → followup_sent → rejected → accepted

    ats_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    tailored_resume_text: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Email tracking
    email_sent_to: Mapped[str | None] = mapped_column(String(255), nullable=True)
    email_sent_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    email_subject: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # Interview tracking
    interview_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    interview_type: Mapped[str | None] = mapped_column(
        String(50), nullable=True
    )  # phone, video, onsite
    interview_notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Follow-up tracking
    followup_count: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    last_followup_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    next_followup_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # Metadata
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # Relationships
    user = relationship("User", backref="auto_applications")
    job = relationship("Job")


class ResumeTemplate(Base):
    """
    Stores user's base resume as a JSON template.
    Used by AI to generate tailored resumes for each job.
    """

    __tablename__ = "resume_templates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False, default="Default")
    category: Mapped[str] = mapped_column(
        String(50), nullable=False, default="general", server_default="general"
    )
    style: Mapped[str] = mapped_column(
        String(50), nullable=False, default="modern", server_default="modern"
    )
    content: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_public: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default="false"
    )
    download_count: Mapped[int] = mapped_column(
        Integer, default=0, server_default="0"
    )
    template_json: Mapped[str] = mapped_column(
        Text, nullable=False
    )  # JSON structure
    work_experience: Mapped[str | None] = mapped_column(Text, nullable=True)
    education: Mapped[str | None] = mapped_column(Text, nullable=True)
    skills: Mapped[str | None] = mapped_column(Text, nullable=True)
    certifications: Mapped[str | None] = mapped_column(Text, nullable=True)
    projects: Mapped[str | None] = mapped_column(Text, nullable=True)

    is_default: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default="false"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    user = relationship("User", backref="resume_templates")
