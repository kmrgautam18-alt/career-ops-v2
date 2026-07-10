from __future__ import annotations

from pathlib import Path
import re


RESOURCE_DIR = (
    Path(__file__).parent.parent
    / "resources"
    / "skills"
)


class SkillExtractor:
    """
    Production-grade Skill Extractor.

    Current Version
    ---------------
    - Knowledge Base Matching
    - Regex Boundary Matching
    - Category Detection

    Future Versions
    ---------------
    - Embedding Search
    - Ontology Matching
    - LLM Extraction
    - Knowledge Graph
    - Semantic Similarity

    NOTE

    Public output contract MUST remain stable.

    Every extractor (Rule, AI, Hybrid) must return:

    [
        {
            "name": "...",
            "category": "...",
            "confidence": ...,
            "source": "...",
        }
    ]
    """

    def __init__(self):

        self.skills: set[str] = set()

        self.skill_categories: dict[str, str] = {}

        self._load_knowledge_base()

    # ---------------------------------------------------------
    # Knowledge Base
    # ---------------------------------------------------------

    def _load_knowledge_base(self) -> None:
        """
        Load every skill only once during startup.

        Creates:

            self.skills

            self.skill_categories
        """

        if not RESOURCE_DIR.exists():
            return

        for file in RESOURCE_DIR.glob("*.txt"):

            category = file.stem.replace("_", " ").title()

            with open(
                file,
                "r",
                encoding="utf-8",
            ) as f:

                for line in f:

                    skill = line.strip()

                    if not skill:
                        continue

                    self.skills.add(skill)

                    self.skill_categories[skill] = category

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def extract(
        self,
        text: str,
    ) -> list[dict]:
        """
        Extract normalized skills.

        Returns
        -------

        [
            {
                "name": "Docker",
                "category": "Devops",
                "confidence": 1.0,
                "source": "knowledge_base",
            }
        ]
        """

        if not text:
            return []

        normalized = text.lower()

        results: list[dict] = []

        found = set()

        for skill in self.skills:

            pattern = (
                r"\b"
                + re.escape(skill.lower())
                + r"\b"
            )

            if re.search(pattern, normalized):

                found.add(skill)

        for skill in sorted(found):

            results.append(
                {
                    "name": skill,
                    "category": self.skill_categories.get(
                        skill
                    ),
                    "confidence": 1.0,
                    "source": "knowledge_base",
                }
            )

        return results


# ---------------------------------------------------------
# Singleton
# ---------------------------------------------------------

_default_extractor = SkillExtractor()


def extract_skills(
    text: str,
) -> list[dict]:
    """
    Stable public helper.

    Future AI implementations should replace only
    the internal extractor without changing callers.
    """

    return _default_extractor.extract(text)