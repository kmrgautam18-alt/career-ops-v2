from __future__ import annotations

from backend.app.services.ai.interview.difficulty_engine import (
    DifficultyEngine,
)
from backend.app.services.ai.interview.models import (
    InterviewReport,
)
from backend.app.services.ai.interview.question_generator import (
    QuestionGenerator,
)


class InterviewService:
    """
    Public service for generating
    interview questions.
    """

    @staticmethod
    def generate_questions(
        skills: list[str],
        difficulty: str = "All",
    ) -> InterviewReport:

        report = QuestionGenerator.generate(skills)

        report.questions = DifficultyEngine.filter(
            report.questions,
            difficulty,
        )

        return report