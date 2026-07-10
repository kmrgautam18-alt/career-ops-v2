from __future__ import annotations

from enum import Enum

from backend.app.services.experience_extractor.company_detector import (
    detect_companies,
)
from backend.app.services.experience_extractor.date_parser import (
    parse_date,
)
from backend.app.services.experience_extractor.designation_detector import (
    detect_designations,
)
from backend.app.services.experience_extractor.location_detector import (
    detect_locations,
)


class LineType(str, Enum):

    COMPANY = "company"

    DESIGNATION = "designation"

    LOCATION = "location"

    DATE = "date"

    DESCRIPTION = "description"

    EMPTY = "empty"


def classify_line(
    line: str,
) -> LineType:

    line = line.strip()

    if not line:
        return LineType.EMPTY

    if detect_companies(line):
        return LineType.COMPANY

    if detect_designations(line):
        return LineType.DESIGNATION

    if detect_locations(line):
        return LineType.LOCATION

    if parse_date(line):
        return LineType.DATE

    if "-" in line:

        left, _, right = line.partition("-")

        if (
            parse_date(left.strip())
            or parse_date(right.strip())
        ):
            return LineType.DATE

    return LineType.DESCRIPTION