from backend.app.services.ai.ats.section_analyzer import (
    SectionAnalyzer,
)


def test_section_analyzer():
    score, missing = SectionAnalyzer.analyze(
        """
Summary

Experience

Skills
"""
    )

    assert score == 75.0

    assert missing == [
        "Education",
    ]