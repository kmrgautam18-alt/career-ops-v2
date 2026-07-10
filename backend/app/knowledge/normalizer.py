from backend.app.knowledge.entity import Entity


class Normalizer:
    """
    Normalizes extracted entities before
    storing them in the knowledge engine.
    """

    def normalize(self, entity: Entity) -> Entity:
        """
        Normalize one entity.
        """

        entity.value = entity.value.strip()

        entity.value = " ".join(entity.value.split())

        return entity