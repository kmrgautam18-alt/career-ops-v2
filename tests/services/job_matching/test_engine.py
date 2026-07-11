from backend.app.services.job_matching.engine import JobMatchingEngine


def test_job_matching_engine():

    result = JobMatchingEngine.match(
        resume_skills=["Python", "Docker", "Linux"],
        job_skills=["Python", "Docker", "Kubernetes"],

        candidate_years=5,
        required_years=4,

        candidate_degree="Bachelor",
        required_degree="Bachelor",

        candidate_certifications=["AZ-104"],
        required_certifications=["AZ-104"],

        candidate_location="Bangalore",
        job_location="Bangalore",

        remote=False,

        resume_text="Python Docker Linux",
        job_text="Python Docker Kubernetes",
    )

    assert result.overall_score > 0

    assert result.skill.score > 0

    assert result.experience.score == 100

    assert result.education.score == 100

    assert result.certification.score == 100