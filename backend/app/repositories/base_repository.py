from __future__ import annotations

import logging
from typing import Any, Generic, TypeVar

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):  # noqa: UP046
    """
    Base repository for all repositories.

    Responsibilities
    ----------------
    - Database session management
    - Transaction management
    - Logging
    - CRUD helpers
    - Bulk operations
    - Error handling

    All repositories should inherit from this class.
    """

    def __init__(self, db: Session):

        self.db = db

    # ==========================================================
    # Transaction Helpers
    # ==========================================================

    def commit(self) -> None:
        """
        Commit current transaction.
        """

        try:

            self.db.commit()

        except SQLAlchemyError:

            self.db.rollback()

            logger.exception("Database commit failed.")

            raise

    def rollback(self) -> None:
        """
        Rollback current transaction.
        """

        self.db.rollback()

    def flush(self) -> None:
        """
        Flush pending SQL statements.
        """

        self.db.flush()

    def refresh(
        self,
        instance: ModelType,
    ) -> None:
        """
        Refresh ORM object.
        """

        self.db.refresh(instance)

    # ==========================================================
    # CRUD Helpers
    # ==========================================================

    def add(
        self,
        instance: ModelType,
        auto_commit: bool = True,
    ) -> ModelType:
        """
        Add ORM object.
        """

        self.db.add(instance)

        if auto_commit:

            self.commit()

            self.refresh(instance)

        return instance

    def add_all(
        self,
        instances: list[ModelType],
        auto_commit: bool = True,
    ) -> list[ModelType]:
        """
        Bulk add ORM objects.
        """

        self.db.add_all(instances)

        if auto_commit:

            self.commit()

        return instances

    def delete(
        self,
        instance: ModelType,
        auto_commit: bool = True,
    ) -> None:
        """
        Delete ORM object.
        """

        self.db.delete(instance)

        if auto_commit:

            self.commit()

    # ==========================================================
    # Generic Helpers
    # ==========================================================

    def get_by_id(
        self,
        model: type[ModelType],
        object_id: Any,
    ) -> ModelType | None:
        """
        Find object by primary key.
        """

        return self.db.get(
            model,
            object_id,
        )

    def exists(
        self,
        model: type[ModelType],
        **filters: Any,
    ) -> bool:
        """
        Check if object exists.
        """

        query = self.db.query(model)

        for key, value in filters.items():

            query = query.filter(
                getattr(model, key) == value
            )

        return query.first() is not None

    # ==========================================================
    # Context Helper
    # ==========================================================

    def transaction(self):
        """
        Transaction context.

        Example

        with repo.transaction():
            ...
        """

        return self.db.begin()