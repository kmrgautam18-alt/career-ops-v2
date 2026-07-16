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
    """Public service for generating interview questions."""

    @staticmethod
    def generate_questions(
        job_title: str,
        company: str,
        difficulty: str = "medium",
    ) -> InterviewReport:
        """Generate questions based on job title and company using AI."""
        report = QuestionGenerator.generate(
            job_title=job_title,
            company=company,
            difficulty=difficulty,
        )

        report.questions = DifficultyEngine.filter(
            report.questions,
            difficulty,
        )

        return report

    @staticmethod
    def generate_questions_from_skills(
        skills: list[str],
        difficulty: str = "All",
    ) -> InterviewReport:
        """Generate questions based on skills list (fallback)."""
        from backend.app.services.ai.interview.question_bank import (
            QUESTION_BANK,
        )

        questions = []
        for skill in skills:
            entries = QUESTION_BANK.get(skill.lower())
            if not entries:
                continue
            for item in entries:
                questions.append({
                    "question": item["question"],
                    "category": skill.title(),
                    "difficulty": item["difficulty"],
                })

        from backend.app.services.ai.interview.models import (
            InterviewQuestion,
        )

        report = InterviewReport(
            questions=[
                InterviewQuestion(
                    question=q["question"],
                    category=q["category"],
                    difficulty=q["difficulty"],
                )
                for q in questions
            ]
        )

        report.questions = DifficultyEngine.filter(
            report.questions,
            difficulty,
        )

        return report
