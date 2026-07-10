from __future__ import annotations

import logging

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from backend.app.models.resume_skill import ResumeSkill
from backend.app.repositories.base_repository import BaseRepository

logger = logging.getLogger(__name__)


class ResumeSkillRepository(BaseRepository[ResumeSkill]):
    """
    Repository responsible for persisting normalized resume skills.

    Features
    --------
    - Bulk Insert
    - PostgreSQL UPSERT
    - Duplicate Protection
    - Structured Logging

    NOTE
    ----
    Transaction management is intentionally handled by the
    Service Layer (Unit of Work).

    Repository should NOT start its own transaction.
    """

    def __init__(self, db: Session):
        super().__init__(db)

    def save_skills(
        self,
        resume_id: int,
        skills: list[dict],
    ) -> None:
        """
        Persist extracted skills.

        Expected input:

        [
            {
                "name": "Docker",
                "category": "DevOps",
                "confidence": 1.0,
                "source": "knowledge_base",
            }
        ]
        """

        if not skills:
            return

        rows = []

        for skill in skills:
            rows.append(
                {
                    "resume_id": resume_id,
                    "skill_name": skill["name"],
                    "category": skill.get("category"),
                    "confidence": skill.get(
                        "confidence",
                        1.0,
                    ),
                    "source": skill.get(
                        "source",
                        "knowledge_base",
                    ),
                }
            )

        statement = (
            insert(ResumeSkill)
            .values(rows)
            .on_conflict_do_nothing(
                constraint="uq_resume_skill",
            )
        )

        try:
            self.db.execute(statement)

            logger.info(
                "Saved %d skills for resume %d",
                len(rows),
                resume_id,
            )

        except SQLAlchemyError:
            self.db.rollback()

            logger.exception(
                "Failed saving skills for resume %d",
                resume_id,
            )

            raise