from __future__ import annotations

import re

from backend.app.services.experience_extractor.company_detector import (
    detect_companies,
)
from backend.app.services.experience_extractor.designation_detector import (
    detect_designations,
)
from backend.app.services.experience_extractor.location_detector import (
    detect_locations,
)
from backend.app.services.experience_extractor.employment_type_detector import (
    detect_employment_type,
)


DATE_PATTERN = re.compile(
    r".+\s*[-–]\s*.+",
    re.IGNORECASE,
)


def extract_description(
    block: str,
) -> str | None:
    """
    Extract work description from an
    experience block by removing all
    structured information.

    Current
    -------
    Removes

    - Company
    - Designation
    - Location
    - Employment Type
    - Date Range

    Remaining text becomes description.
    """

    if not block:
        return None

    companies = set(
        detect_companies(block)
    )

    designations = set(
        detect_designations(block)
    )

    locations = set(
        detect_locations(block)
    )

    employment = detect_employment_type(
        block,
    )

    description_lines: list[str] = []

    for line in block.splitlines():

        line = line.strip()

        if not line:
            continue

        if line in companies:
            continue

        if line in designations:
            continue

        if line in locations:
            continue

        if employment and line.lower() == employment.value.lower():
            continue

        if DATE_PATTERN.match(line):
            continue

        description_lines.append(line)

    if not description_lines:
        return None

    return "\n".join(description_lines)