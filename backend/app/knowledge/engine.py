from __future__ import annotations

from backend.app.knowledge.cache import (
    knowledge_cache,
)
from backend.app.knowledge.providers.file_provider import (
    FileKnowledgeProvider,
)


class KnowledgeEngine:
    """
    Central knowledge gateway.
    """

    def __init__(self) -> None:
        self.provider = FileKnowledgeProvider()

    # ==========================================================
    # Experience
    # ==========================================================

    def designations(self) -> list[str]:
        return knowledge_cache.get_or_load(
            "designations",
            self.provider.get_designations,
        )

    def companies(self) -> list[str]:
        return knowledge_cache.get_or_load(
            "companies",
            self.provider.get_companies,
        )

    def skills(
        self,
        category: str | None = None,
    ) -> list[str]:

        key = f"skills:{category or 'all'}"

        return knowledge_cache.get_or_load(
            key,
            lambda: self.provider.get_skills(category),
        )

    def skill_categories(self) -> list[str]:
        return knowledge_cache.get_or_load(
            "skill_categories",
            self.provider.get_skill_categories,
        )

    def locations(self) -> list[str]:
        return knowledge_cache.get_or_load(
            "locations",
            self.provider.get_locations,
        )

    # ==========================================================
    # Education
    # ==========================================================

    def degrees(self) -> list[str]:
        return knowledge_cache.get_or_load(
            "degrees",
            self.provider.get_degrees,
        )

    def specializations(self) -> list[str]:
        return knowledge_cache.get_or_load(
            "specializations",
            self.provider.get_specializations,
        )

    # ==========================================================

    def clear_cache(self) -> None:
        knowledge_cache.clear()


knowledge_engine = KnowledgeEngine()