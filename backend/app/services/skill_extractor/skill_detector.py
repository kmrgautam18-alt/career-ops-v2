from __future__ import annotations

from backend.app.knowledge.engine import (
    knowledge_engine,
)
from backend.app.services.common.knowledge_matcher import (
    match_knowledge,
)


def detect_skills(
    text: str,
    category: str | None = None,
) -> list[str]:
    """
    Detect skills from resume text.

    Parameters
    ----------
    text:
        Resume text.

    category:
        Optional skill category.

    Examples
    --------
    detect_skills(text)

    detect_skills(
        text,
        category="cloud",
    )
    """

    return match_knowledge(
        text=text,
        knowledge=knowledge_engine.skills(
            category,
        ),
    )