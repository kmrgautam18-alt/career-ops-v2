from backend.app.services.ai.ats.keyword_analyzer import KeywordAnalyzer


def test_keyword_analyzer():
    score, missing = KeywordAnalyzer.analyze(
        resume_text="""
Python
Docker
Linux
Git
""",
        keywords=[
            "Python",
            "Docker",
            "Terraform",
        ],
    )

    assert score == 66.67
    assert missing == ["Terraform"]