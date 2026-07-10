from __future__ import annotations

from backend.app.knowledge.engine import (
    knowledge_engine,
)
from backend.app.services.common.knowledge_matcher import (
    match_knowledge,
)


def detect_degrees(
    text: str,
) -> list[str]:
    """
    Detect education degrees using
    the shared Knowledge Matcher.

    Examples
    --------
    Bachelor of Technology
    B.Tech
    MBA
    Master of Business Administration
    """

    return match_knowledge(
        text=text,
        knowledge=knowledge_engine.degrees(),
    )