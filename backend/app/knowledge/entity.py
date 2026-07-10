from dataclasses import dataclass, field
from typing import Any

from backend.app.knowledge.entity_types import EntityType


@dataclass(slots=True)
class Entity:
    """
    Universal entity used across Career-Ops.

    Every piece of extracted information is represented
    as an Entity.
    """

    value: str

    entity_type: EntityType

    confidence: float = 1.0

    source: str = "parser"

    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "value": self.value,
            "entity_type": self.entity_type.value,
            "confidence": self.confidence,
            "source": self.source,
            "metadata": self.metadata,
        }