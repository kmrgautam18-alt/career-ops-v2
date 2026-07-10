from __future__ import annotations

import logging

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from backend.app.models.resume_experience import ResumeExperience
from backend.app.repositories.base_repository import BaseRepository

logger = logging.getLogger(__name__)


class ResumeExperienceRepository(
    BaseRepository[ResumeExperience]
):
    """
    Repository responsible for persisting
    structured resume experiences.

    Features
    --------
    - Bulk Insert
    - Structured Logging
    - Repository Pattern

    NOTE
    ----
    Transaction management is handled by
    the Service Layer.
    """

    def __init__(self, db: Session):
        super().__init__(db)

    def save_many(
        self,
        resume_id: int,
        experiences: list[dict],
    ) -> None:
        """
        Persist extracted experiences.

        Expected input

        [
            {
                "company": "...",
                "designation": "...",
                "employment_type": "...",
                "location": "...",
                "start_date": ...,
                "end_date": ...,
                "currently_working": False,
                "duration_months": 24,
                "description": "...",
                "confidence": 1.0,
                "source": "knowledge_base",
            }
        ]
        """

        if not experiences:
            return

        try:

            objects = []

            for exp in experiences:

                objects.append(
                    ResumeExperience(
                        resume_id=resume_id,
                        company=exp.get("company"),
                        designation=exp.get("designation"),
                        employment_type=exp.get(
                            "employment_type"
                        ),
                        location=exp.get("location"),
                        start_date=exp.get("start_date"),
                        end_date=exp.get("end_date"),
                        currently_working=exp.get(
                            "currently_working",
                            False,
                        ),
                        duration_months=exp.get(
                            "duration_months"
                        ),
                        description=exp.get(
                            "description"
                        ),
                        confidence=exp.get(
                            "confidence",
                            1.0,
                        ),
                        source=exp.get(
                            "source",
                            "knowledge_base",
                        ),
                    )
                )

            self.db.add_all(objects)

            logger.info(
                "Saved %d experiences for resume %d",
                len(objects),
                resume_id,
            )

        except SQLAlchemyError:

            self.db.rollback()

            logger.exception(
                "Failed saving experiences for resume %d",
                resume_id,
            )

            raise

    def find_by_resume(
        self,
        resume_id: int,
    ) -> list[ResumeExperience]:
        """
        Return all experiences belonging
        to a resume.
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
        of a resume.
        """

        return (
            self.db.query(ResumeExperience)
            .filter(
                ResumeExperience.resume_id == resume_id
            )
            .delete()
        )