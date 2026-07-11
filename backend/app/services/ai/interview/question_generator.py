from __future__ import annotations

from backend.app.services.ai.interview.models import (
    InterviewQuestion,
    InterviewReport,
)
from backend.app.services.ai.interview.question_bank import (
    QUESTION_BANK,
)


class QuestionGenerator:
    """
    Generates interview questions based on
    detected technologies.
    """

    @staticmethod
    def generate(
        skills: list[str],
    ) -> InterviewReport:

        questions: list[InterviewQuestion] = []

        for skill in skills:

            entries = QUESTION_BANK.get(skill.lower())

            if not entries:
                continue

            for item in entries:

                questions.append(
                    InterviewQuestion(
                        question=item["question"],
                        category=skill.title(),
                        difficulty=item["difficulty"],
                    )
                )

        return InterviewReport(
            questions=questions,
        )