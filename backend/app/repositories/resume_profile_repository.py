from sqlalchemy.orm import Session

from backend.app.models.resume_profile import ResumeProfile
from backend.app.repositories.base_repository import BaseRepository


class ResumeProfileRepository(BaseRepository[ResumeProfile]):
    """
    Repository responsible for ResumeProfile persistence.
    """

    def __init__(self, db: Session):

        super().__init__(db)

    def create(
        self,
        resume_id: int,
        profile: dict,
    ) -> ResumeProfile:
        """
        Create and persist a resume profile.
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

        return self.add(resume_profile)