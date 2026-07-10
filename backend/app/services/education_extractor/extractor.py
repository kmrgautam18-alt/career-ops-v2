from __future__ import annotations

from backend.app.services.education_extractor.education_builder import (
    build_education,
)
from backend.app.services.education_extractor.education_models import (
    EducationRecord,
)


def split_education_blocks(
    text: str,
) -> list[str]:
    """
    Split education section into
    logical education blocks.

    Current strategy:
    -----------------
    Blank line separates records.

    Future:
    -------
    State machine (same as Experience Extractor)
    """

    if not text:
        return []

    return [
        block.strip()
        for block in text.split("\n\n")
        if block.strip()
    ]


def extract_education(
    text: str,
) -> list[EducationRecord]:
    """
    Extract all education records.
    """

    records: list[EducationRecord] = []

    for block in split_education_blocks(text):

        record = build_education(block)

        if (
            record.degree
            or record.specialization
        ):
            records.append(record)

    return records