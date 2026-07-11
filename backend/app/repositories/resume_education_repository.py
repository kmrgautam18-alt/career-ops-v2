from __future__ import annotations

import logging

from sqlalchemy.orm import Session

from backend.app.models.resume_education import ResumeEducation
from backend.app.repositories.base_repository import BaseRepository
from backend.app.services.education_extractor.education_models import (
    EducationRecord,
)

logger = logging.getLogger(__name__)


class ResumeEducationRepository(
    BaseRepository[ResumeEducation]
):
    """
    Repository responsible for persisting
    structured education records.
    """

    def __init__(
        self,
        db: Session,
    ):
        super().__init__(db)

    def save_many(
        self,
        resume_id: int,
        educations: list[EducationRecord],
    ) -> None:
        """
        Persist extracted education.

        Transaction is handled
        by the service layer.
        """

        if not educations:
            return

        objects: list[ResumeEducation] = []

        for education in educations:

            objects.append(
                ResumeEducation(
                    resume_id=resume_id,
                    degree=education.degree,
                    specialization=education.specialization,
                    institution=education.institution,
                    location=education.location,
                    university=education.university,
                    start_date=education.start_date,
                    end_date=education.end_date,
                    grade=education.grade,
                    percentage=education.percentage,
                    cgpa=education.cgpa,
                    currently_studying=education.currently_studying,
                    description=education.description,
                    confidence=education.confidence,
                    source=education.source,
                )
            )

        self.db.add_all(objects)

        logger.info(
            "Saved %d education records for resume %d",
            len(objects),
            resume_id,
        )

    def find_by_resume(
        self,
        resume_id: int,
    ) -> list[ResumeEducation]:
        """
        Return all education records.
        """

        return (
            self.db.query(ResumeEducation)
            .filter(
                ResumeEducation.resume_id == resume_id
            )
            .order_by(
                ResumeEducation.id
            )
            .all()
        )

    def delete_by_resume(
        self,
        resume_id: int,
    ) -> int:
        """
        Delete education records.
        """

        return (
            self.db.query(ResumeEducation)
            .filter(
                ResumeEducation.resume_id == resume_id
            )
            .delete()
        )