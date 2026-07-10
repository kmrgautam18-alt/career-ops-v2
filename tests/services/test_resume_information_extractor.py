from backend.app.services.resume_information_extractor import (
    extract_profile,
)
from backend.app.services.resume_information_models import (
    ResumeInformation,
)


def test_extract_profile_returns_resume_information():
    text = """
    Software Engineer

    Worked at Microsoft from Jan 2020 to Present.
    """

    profile = extract_profile(text)

    assert isinstance(profile, ResumeInformation)