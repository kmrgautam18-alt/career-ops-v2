from __future__ import annotations

import re


PRESENT_KEYWORDS = {
    "present",
    "current",
    "till date",
    "till now",
    "currently",
    "ongoing",
    "now",
}


def normalize_text(
    text: str,
) -> str:
    """
    Normalize text for rule-based matching.

    Current
    -------
    - lowercase
    - collapse whitespace

    Future
    ------
    - unicode normalization
    - punctuation cleanup
    - OCR cleanup
    """

    if not text:
        return ""

    text = text.lower()

    text = re.sub(
        r"\s+",
        " ",
        text,
    )

    return text.strip()


def is_present_text(
    text: str,
) -> bool:
    """
    Returns True if the supplied text
    represents an ongoing employment.
    """

    normalized = normalize_text(text)

    return normalized in PRESENT_KEYWORDS