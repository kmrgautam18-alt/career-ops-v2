from __future__ import annotations

from backend.app.knowledge.engine import (
    knowledge_engine,
)
from backend.app.services.common.knowledge_matcher import (
    match_knowledge,
)


def detect_specializations(
    text: str,
) -> list[str]:
    """
    Detect education specializations using
    the shared Knowledge Matcher.

    Examples
    --------
    Computer Science
    Artificial Intelligence
    Information Technology
    Data Science
    """

    return match_knowledge(
        text=text,
        knowledge=knowledge_engine.specializations(),
    )