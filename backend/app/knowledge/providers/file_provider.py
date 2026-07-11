from __future__ import annotations

from pathlib import Path

from backend.app.knowledge.providers.base_provider import (
    BaseKnowledgeProvider,
)

RESOURCE_ROOT = (
    Path(__file__).parent.parent.parent
    / "resources"
)


class FileKnowledgeProvider(
    BaseKnowledgeProvider,
):
    """
    Reads knowledge from resource files.

    Current
    -------
    TXT files

    Future
    ------
    Database
    AI
    """

    def _read_lines(
        self,
        path: Path,
    ) -> list[str]:

        if not path.exists():
            return []

        values: list[str] = []

        with open(
            path,
            encoding="utf-8",
        ) as file:

            for line in file:

                value = line.strip()

                if value:
                    values.append(value)

        return sorted(
            set(values),
            key=len,
            reverse=True,
        )

    # ==========================================================
    # Experience
    # ==========================================================

    def get_designations(
        self,
    ) -> list[str]:

        return self._read_lines(
            RESOURCE_ROOT
            / "designations"
            / "common_designations.txt"
        )

    def get_companies(
        self,
    ) -> list[str]:

        return self._read_lines(
            RESOURCE_ROOT
            / "companies"
            / "known_companies.txt"
        )

    def get_skills(
        self,
        category: str | None = None,
    ) -> list[str]:

        skill_root = (
            RESOURCE_ROOT
            / "skills"
        )

        if category:

            return self._read_lines(
                skill_root
                / f"{category}.txt"
            )

        skills: list[str] = []

        for file in skill_root.glob("*.txt"):

            skills.extend(
                self._read_lines(file)
            )

        return sorted(
            set(skills),
            key=len,
            reverse=True,
        )

    def get_skill_categories(
        self,
    ) -> list[str]:

        return self._read_lines(
            RESOURCE_ROOT
            / "skills"
            / "categories.txt"
        )

    def get_locations(
        self,
    ) -> list[str]:

        return self._read_lines(
            RESOURCE_ROOT
            / "locations"
            / "common_locations.txt"
        )

    # ==========================================================
    # Education
    # ==========================================================

    def get_degrees(
        self,
    ) -> list[str]:

        return self._read_lines(
            RESOURCE_ROOT
            / "education"
            / "common_degrees.txt"
        )

    def get_specializations(
        self,
    ) -> list[str]:

        return self._read_lines(
            RESOURCE_ROOT
            / "education"
            / "common_specializations.txt"
        )