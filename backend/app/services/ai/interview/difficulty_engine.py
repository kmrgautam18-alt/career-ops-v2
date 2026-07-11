from __future__ import annotations

from backend.app.services.ai.interview.models import (
    InterviewQuestion,
)


class DifficultyEngine:
    """
    Filters interview questions
    by difficulty level.
    """

    @staticmethod
    def filter(
        questions: list[InterviewQuestion],
        difficulty: str,
    ) -> list[InterviewQuestion]:

        if difficulty.lower() == "all":
            return questions

        return [
            question
            for question in questions
            if question.difficulty.lower()
            == difficulty.lower()
        ]