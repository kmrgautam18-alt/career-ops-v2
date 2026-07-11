from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ResumeProfileRecord:
    """
    Structured profile extracted from resume.
    """

    full_name: str | None = None

    email: str | None = None

    phone: str | None = None

    linkedin: str | None = None

    github: str | None = None

    portfolio: str | None = None

    location: str | None = None