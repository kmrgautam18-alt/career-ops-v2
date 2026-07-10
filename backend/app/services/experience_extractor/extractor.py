from __future__ import annotations

from backend.app.services.experience_extractor.experience_builder import (
    build_experience,
)
from backend.app.services.experience_extractor.experience_models import (
    ExperienceRecord,
)
from backend.app.services.experience_extractor.line_classifier import (
    LineType,
    classify_line,
)


def split_experience_blocks(
    text: str,
) -> list[str]:
    """
    Split resume into logical experience blocks using
    a lightweight state machine.

    New block starts when a COMPANY line is found
    after a DATE has already been seen.
    """

    if not text:
        return []

    blocks: list[str] = []

    current: list[str] = []

    seen_date = False

    for raw_line in text.splitlines():

        line = raw_line.strip()

        if not line:
            continue

        line_type = classify_line(line)

        # --------------------------------------------------
        # New experience starts
        # --------------------------------------------------

        if (
            line_type == LineType.COMPANY
            and seen_date
            and current
        ):

            blocks.append(
                "\n".join(current)
            )

            current = []

            seen_date = False

        current.append(line)

        if line_type == LineType.DATE:

            seen_date = True

    if current:

        blocks.append(
            "\n".join(current)
        )

    return blocks


def extract_experiences(
    text: str,
) -> list[ExperienceRecord]:
    """
    Extract all experience records from resume.
    """

    experiences: list[ExperienceRecord] = []

    for block in split_experience_blocks(text):

        record = build_experience(block)

        if record.company or record.designation:

            experiences.append(record)

    return experiences
