from backend.app.services.job_matching.matchers.skill_matcher import SkillMatcher


def test_skill_matcher():
    result = SkillMatcher.match(
        candidate_skills=[
            "Linux",
            "Docker",
            "Git",
        ],
        required_skills=[
            "Linux",
            "Docker",
            "Kubernetes",
            "Git",
        ],
    )

    assert result.score == 75.0

    assert result.matched == [
        "docker",
        "git",
        "linux",
    ]

    assert result.missing == [
        "kubernetes",
    ]

    assert len(result.reasons) == 1