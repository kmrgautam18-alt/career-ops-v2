from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.resume_profile import ResumeProfile
from backend.app.repositories.base_repository import BaseRepository


class ResumeProfileRepository(
    BaseRepository[ResumeProfile]
):
    """
    Repository responsible for
    ResumeProfile persistence.
    """

    def __init__(
        self,
        db: Session,
    ):
        super().__init__(db)

    def create(
        self,
        resume_id: int,
        profile: dict,
    ) -> ResumeProfile:
        """
        Create a resume profile.

        Transaction is handled
        by the service layer.
        """

        resume_profile = ResumeProfile(
            resume_id=resume_id,
            full_name=profile.get("full_name"),
            email=profile.get("email"),
            phone=profile.get("phone"),
            linkedin=profile.get("linkedin"),
            github=profile.get("github"),
            portfolio=profile.get("portfolio"),
            location=profile.get("location"),
        )

        self.db.add(resume_profile)

        self.db.flush()
        self.db.refresh(resume_profile)

        return resume_profile

    def find_by_resume(
        self,
        resume_id: int,
    ) -> ResumeProfile | None:
        """
        Return the profile associated
        with a resume.
        """

        return self.db.scalar(
            select(
                ResumeProfile,
            ).where(
                ResumeProfile.resume_id == resume_id,
            )
        )

    def delete_by_resume(
        self,
        resume_id: int,
    ) -> int:
        """
        Delete profile
        belonging to a resume.
        """

        return (
            self.db.query(
                ResumeProfile,
            )
            .filter(
                ResumeProfile.resume_id == resume_id,
            )
            .delete()
        )