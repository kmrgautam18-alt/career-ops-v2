from __future__ import annotations

import re


def match_knowledge(
    text: str,
    knowledge: list[str],
) -> list[str]:
    """
    Generic matcher for every knowledge-based detector.

    Features
    --------
    - Case insensitive
    - Longest match wins
    - Removes duplicates
    - Removes nested matches

    Examples
    --------
    Computer Science
    Computer Science and Engineering

    Returns only

    Computer Science and Engineering
    """

    if not text:
        return []

    text_lower = text.lower()

    matches: list[str] = []

    for value in knowledge:

        pattern = (
            r"\b"
            + re.escape(
                value.lower(),
            )
            + r"\b"
        )

        if re.search(
            pattern,
            text_lower,
            re.IGNORECASE,
        ):
            matches.append(value)

    if not matches:
        return []

    # ------------------------------------------
    # Remove duplicates while preserving order
    # ------------------------------------------

    matches = list(
        dict.fromkeys(matches)
    )

    # ------------------------------------------
    # Longest match wins
    # ------------------------------------------

    filtered: list[str] = []

    for candidate in matches:

        keep = True

        for other in matches:

            if (
                candidate != other
                and candidate.lower()
                in other.lower()
            ):
                keep = False
                break

        if keep:
            filtered.append(candidate)

    return filtered