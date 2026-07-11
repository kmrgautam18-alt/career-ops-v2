from __future__ import annotations

import re

from backend.app.services.profile_extractor.models import (
    ResumeProfileRecord,
)

EMAIL_PATTERN = re.compile(
    r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
)

PHONE_PATTERN = re.compile(
    r"(?:\+91[- ]?)?[6-9]\d{9}"
)

LINKEDIN_PATTERN = re.compile(
    r"(https?://)?(www\.)?linkedin\.com/in/[^\s]+",
    re.IGNORECASE,
)

GITHUB_PATTERN = re.compile(
    r"(https?://)?(www\.)?github\.com/[^\s]+",
    re.IGNORECASE,
)


def extract_profile(
    text: str,
) -> ResumeProfileRecord:
    """
    Lightweight profile extractor.

    AI extractor can replace this later.
    """

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    profile = ResumeProfileRecord()

    if lines:
        profile.full_name = lines[0]

    email = EMAIL_PATTERN.search(text)

    if email:
        profile.email = email.group()

    phone = PHONE_PATTERN.search(text)

    if phone:
        profile.phone = phone.group()

    linkedin = LINKEDIN_PATTERN.search(text)

    if linkedin:
        profile.linkedin = linkedin.group()

    github = GITHUB_PATTERN.search(text)

    if github:
        profile.github = github.group()

    return profile