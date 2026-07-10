from __future__ import annotations

from abc import ABC
from abc import abstractmethod


class BaseKnowledgeProvider(ABC):
    """
    Base interface for every knowledge provider.
    """

    # ==========================================================
    # Experience
    # ==========================================================

    @abstractmethod
    def get_designations(self) -> list[str]:
        ...

    @abstractmethod
    def get_companies(self) -> list[str]:
        ...

    @abstractmethod
    def get_skills(
        self,
        category: str | None = None,
    ) -> list[str]:
        ...

    @abstractmethod
    def get_locations(self) -> list[str]:
        ...

    # ==========================================================
    # Education
    # ==========================================================

    @abstractmethod
    def get_degrees(self) -> list[str]:
        ...

    @abstractmethod
    def get_specializations(self) -> list[str]:
        ...

    @abstractmethod
    def get_skill_categories(self,) -> list[str]:
        ...    