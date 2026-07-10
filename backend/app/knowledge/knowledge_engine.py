from collections import defaultdict

from backend.app.knowledge.entity import Entity
from backend.app.knowledge.entity_types import EntityType


class KnowledgeEngine:
    """
    Central knowledge engine.

    Every parser sends extracted entities here.

    The engine stores, merges, filters and later
    normalizes all information.
    """

    def __init__(self) -> None:
        self._entities: list[Entity] = []

    def add(self, entity: Entity) -> None:
        """
        Add one entity.
        """
        self._entities.append(entity)

    def add_many(self, entities: list[Entity]) -> None:
        """
        Add multiple entities.
        """
        self._entities.extend(entities)

    def all(self) -> list[Entity]:
        """
        Return every entity.
        """
        return list(self._entities)

    def by_type(self, entity_type: EntityType) -> list[Entity]:
        """
        Return entities of one type.
        """
        return [
            entity
            for entity in self._entities
            if entity.entity_type == entity_type
        ]

    def grouped(self) -> dict[EntityType, list[Entity]]:
        """
        Group entities by type.
        """
        groups: dict[EntityType, list[Entity]] = defaultdict(list)

        for entity in self._entities:
            groups[entity.entity_type].append(entity)

        return dict(groups)

    def clear(self) -> None:
        """
        Reset engine.
        """
        self._entities.clear()