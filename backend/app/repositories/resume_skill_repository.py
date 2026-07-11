from __future__ import annotations

import logging

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from backend.app.models.resume_skill import ResumeSkill
from backend.app.repositories.base_repository import BaseRepository
from backend.app.services.skill_extractor.skill_models import (
    SkillRecord,
)

logger = logging.getLogger(__name__)


class ResumeSkillRepository(BaseRepository[ResumeSkill]):
    """
    Repository responsible for persisting normalized resume skills.
    """

    def __init__(
        self,
        db: Session,
    ):
        super().__init__(db)

    def save_skills(
        self,
        resume_id: int,
        skills: list[SkillRecord],
    ) -> None:
        """
        Persist extracted skills.
        """

        if not skills:
            return

        rows = []

        for skill in skills:

            rows.append(
                {
                    "resume_id": resume_id,
                    "skill_name": skill.name,
                    "category": skill.category,
                    "confidence": skill.confidence,
                    "source": skill.source,
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

    def find_by_resume(
        self,
        resume_id: int,
    ) -> list[ResumeSkill]:
        """
        Return all skills belonging to a resume.
        """

        return list(
            self.db.scalars(
                select(ResumeSkill)
                .where(
                    ResumeSkill.resume_id == resume_id,
                )
                .order_by(
                    ResumeSkill.skill_name,
                )
            ).all()
        )