from __future__ import annotations

import logging

from sqlalchemy.orm import Session

from backend.app.models.resume_experience import ResumeExperience
from backend.app.repositories.base_repository import BaseRepository
from backend.app.services.experience_extractor.experience_models import (
    ExperienceRecord,
)

logger = logging.getLogger(__name__)


class ResumeExperienceRepository(
    BaseRepository[ResumeExperience]
):
    """
    Repository responsible for persisting
    structured resume experiences.
    """

    def __init__(
        self,
        db: Session,
    ):
        super().__init__(db)

    def save_many(
        self,
        resume_id: int,
        experiences: list[ExperienceRecord],
    ) -> None:
        """
        Persist extracted experiences.

        Transaction is handled by
        the service layer.
        """

        if not experiences:
            return

        objects: list[ResumeExperience] = []

        for experience in experiences:

            objects.append(
                ResumeExperience(
                    resume_id=resume_id,
                    company=experience.company,
                    designation=experience.designation,
                    employment_type=experience.employment_type,
                    location=experience.location,
                    start_date=experience.start_date,
                    end_date=experience.end_date,
                    currently_working=experience.currently_working,
                    duration_months=experience.duration_months,
                    description=experience.description,
                    confidence=experience.confidence,
                    source=experience.source,
                )
            )

        self.db.add_all(objects)

        logger.info(
            "Saved %d experiences for resume %d",
            len(objects),
            resume_id,
        )

    def find_by_resume(
        self,
        resume_id: int,
    ) -> list[ResumeExperience]:
        """
        Return all experiences
        belonging to a resume.
        """

        return (
            self.db.query(ResumeExperience)
            .filter(
                ResumeExperience.resume_id == resume_id
            )
            .order_by(
                ResumeExperience.start_date.desc()
            )
            .all()
        )

    def delete_by_resume(
        self,
        resume_id: int,
    ) -> int:
        """
        Delete all experiences
        belonging to a resume.
        """

        return (
            self.db.query(ResumeExperience)
            .filter(
                ResumeExperience.resume_id == resume_id
            )
            .delete()
        )