from __future__ import annotations

import re
from datetime import date

MONTH_MAP = {
    "jan": 1,
    "january": 1,
    "feb": 2,
    "february": 2,
    "mar": 3,
    "march": 3,
    "apr": 4,
    "april": 4,
    "may": 5,
    "jun": 6,
    "june": 6,
    "jul": 7,
    "july": 7,
    "aug": 8,
    "august": 8,
    "sep": 9,
    "sept": 9,
    "september": 9,
    "oct": 10,
    "october": 10,
    "nov": 11,
    "november": 11,
    "dec": 12,
    "december": 12,
}


PRESENT_KEYWORDS = {
    "present",
    "current",
    "till date",
    "till now",
    "ongoing",
}


def is_present(value: str) -> bool:
    """
    Returns True if the supplied value represents
    an ongoing employment.
    """

    if not value:
        return False

    return value.strip().lower() in PRESENT_KEYWORDS


def parse_date(value: str) -> date | None:
    """
    Parse common resume date formats.

    Supported formats (V1)

    Jan 2022
    January 2022
    Apr 2024
    April 2024
    2022
    Present
    Current
    Till Date
    """

    if not value:
        return None

    value = value.strip()

    if is_present(value):
        return None

    normalized = value.lower()

    #
    # Month Year
    #
    match = re.fullmatch(
        r"([a-zA-Z]+)\s+(\d{4})",
        normalized,
    )

    if match:

        month_name = match.group(1)
        year = int(match.group(2))

        month = MONTH_MAP.get(month_name)

        if month is not None:
            return date(
                year,
                month,
                1,
            )

    #
    # Year only
    #
    if re.fullmatch(r"\d{4}", normalized):

        return date(
            int(normalized),
            1,
            1,
        )

    return None