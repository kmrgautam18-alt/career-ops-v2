from sqlalchemy.orm import Session

from backend.app.repositories.job_repository_sa import (
    get_job_by_id,
)
from backend.app.repositories.resume_repository_sa import (
    get_resume_by_id,
)
from backend.app.repositories.resume_profile_repository import (
    ResumeProfileRepository,
)
from backend.app.repositories.resume_skill_repository import (
    ResumeSkillRepository,
)
from backend.app.repositories.resume_experience_repository import (
    ResumeExperienceRepository,
)

from backend.app.schemas.job_match_schema import (
    JobMatchResponse,
    MatchComponentResponse,
)

from backend.app.services.job_information_extractor import (
    extract_job_information,
)
from backend.app.services.job_matching.engine import (
    JobMatchingEngine,
)


def match_job(
    db: Session,
    *,
    resume_id: int,
    job_id: int,
) -> JobMatchResponse:
    """
    Match a resume against a job.
    """

    resume = get_resume_by_id(
        db=db,
        resume_id=resume_id,
    )

    if resume is None:
        raise ValueError(
            f"Resume {resume_id} not found."
        )

    job = get_job_by_id(
        db=db,
        job_id=job_id,
    )

    if job is None:
        raise ValueError(
            f"Job {job_id} not found."
        )

    profile_repo = ResumeProfileRepository(db)
    skill_repo = ResumeSkillRepository(db)
    experience_repo = ResumeExperienceRepository(db)

    profile = profile_repo.find_by_resume(
        resume.id,
    )

    skills = skill_repo.find_by_resume(
        resume.id,
    )

    experiences = experience_repo.find_by_resume(
        resume.id,
    )

    job_information = extract_job_information(
        job.description or "",
    )

    resume_skills = [
        skill.skill_name
        for skill in skills
    ]

    total_months = sum(
        exp.duration_months or 0
        for exp in experiences
    )

    candidate_years = round(
        total_months / 12,
        2,
    )

    candidate_location = ""

    if profile:
        candidate_location = (
            profile.location or ""
        )

    result = JobMatchingEngine.match(
        resume_skills=resume_skills,
        job_skills=job_information.skills,
        candidate_years=candidate_years,
        required_years=job_information.required_years,
        candidate_degree="",
        required_degree=job_information.required_degree,
        candidate_certifications=[],
        required_certifications=job_information.certifications,
        candidate_location=candidate_location,
        job_location=job_information.location,
        remote=job_information.remote,
        resume_text=resume.parsed_text or "",
        job_text=job_information.text,
    )

    return JobMatchResponse(
        overall_score=result.overall_score,
        classification=result.classification,
        skill=MatchComponentResponse(
            score=result.skill.score,
            matched=result.skill.matched,
            missing=result.skill.missing,
            reasons=result.skill.reasons,
        ),
        experience=MatchComponentResponse(
            score=result.experience.score,
            matched=result.experience.matched,
            missing=result.experience.missing,
            reasons=result.experience.reasons,
        ),
        education=MatchComponentResponse(
            score=result.education.score,
            matched=result.education.matched,
            missing=result.education.missing,
            reasons=result.education.reasons,
        ),
        certification=MatchComponentResponse(
            score=result.certification.score,
            matched=result.certification.matched,
            missing=result.certification.missing,
            reasons=result.certification.reasons,
        ),
        keyword=MatchComponentResponse(
            score=result.keyword.score,
            matched=result.keyword.matched,
            missing=result.keyword.missing,
            reasons=result.keyword.reasons,
        ),
        location=MatchComponentResponse(
            score=result.location.score,
            matched=result.location.matched,
            missing=result.location.missing,
            reasons=result.location.reasons,
        ),
        strengths=result.strengths,
        weaknesses=result.weaknesses,
        recommendations=result.recommendations,
    )