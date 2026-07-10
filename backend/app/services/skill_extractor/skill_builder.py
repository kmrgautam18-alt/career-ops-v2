from __future__ import annotations

from backend.app.knowledge.engine import (
    knowledge_engine,
)
from backend.app.services.skill_extractor.skill_detector import (
    detect_skills,
)
from backend.app.services.skill_extractor.skill_models import (
    SkillRecord,
)


def _find_category(
    skill: str,
) -> str | None:
    """
    Find the category of a skill.

    Returns
    -------
    Category name if found, otherwise None.
    """

    for category in knowledge_engine.skill_categories():

        file_name = (
            category.lower()
            .replace("/", "_")
            .replace("-", "_")
            .replace(" ", "_")
        )

        skills = knowledge_engine.skills(
            file_name,
        )

        if skill in skills:
            return category

    return None


def build_skills(
    text: str,
) -> list[SkillRecord]:
    """
    Build SkillRecord objects from resume text.
    """

    records: list[SkillRecord] = []

    detected_skills = detect_skills(text)

    for skill in detected_skills:

        records.append(
            SkillRecord(
                name=skill,
                category=_find_category(skill),
            )
        )

    return records