"""Interview question generator powered by Gemini AI."""

from __future__ import annotations

import logging

from backend.app.services.ai.interview.models import (
    InterviewQuestion,
    InterviewReport,
)
from backend.app.services.llm_service import (
    LLMServiceError,
    generate_interview_questions,
)

logger = logging.getLogger(__name__)


class QuestionGenerator:
    """Generates interview questions using AI based on job details."""

    @staticmethod
    def generate(
        job_title: str,
        company: str,
        difficulty: str = "medium",
    ) -> InterviewReport:
        try:
            questions_data = generate_interview_questions(
                job_title=job_title,
                company=company,
                difficulty=difficulty,
                count=8,
            )

            questions = []
            for q in questions_data:
                if isinstance(q, dict) and q.get("question"):
                    questions.append(
                        InterviewQuestion(
                            question=q["question"],
                            category=q.get("category", "General"),
                            difficulty=q.get("difficulty", difficulty),
                        )
                    )

            if not questions:
                return QuestionGenerator._fallback(job_title, company)

            return InterviewReport(questions=questions)

        except LLMServiceError as e:
            logger.warning(f"LLM question generation failed, using fallback: {e}")
            return QuestionGenerator._fallback(job_title, company)

    @staticmethod
    def _fallback(job_title: str, company: str) -> InterviewReport:
        """Rule-based fallback when LLM is unavailable."""
        from backend.app.services.ai.interview.question_bank import (
            QUESTION_BANK,
        )

        questions: list[InterviewQuestion] = []

        # Derive likely skills from job title
        title_lower = job_title.lower()
        likely_skills = []

        if "engineer" in title_lower or "developer" in title_lower:
            likely_skills = ["python", "javascript", "system design", "algorithms"]
        elif "data" in title_lower:
            likely_skills = ["python", "sql", "machine learning", "statistics"]
        elif "devops" in title_lower or "sre" in title_lower:
            likely_skills = ["docker", "kubernetes", "ci/cd", "linux"]
        elif "manager" in title_lower:
            likely_skills = ["leadership", "agile", "strategy", "communication"]
        else:
            likely_skills = ["python", "problem solving", "communication", "algorithms"]

        for skill in likely_skills:
            entries = QUESTION_BANK.get(skill.lower())
            if entries:
                for item in entries[:2]:
                    questions.append(
                        InterviewQuestion(
                            question=item["question"],
                            category=skill.title(),
                            difficulty=item["difficulty"],
                        )
                    )

        if not questions:
            questions = [
                InterviewQuestion(
                    question=f"Tell me about your experience relevant to the {job_title} role at {company}.",
                    category="General",
                    difficulty="medium",
                ),
                InterviewQuestion(
                    question=f"What interests you most about working at {company}?",
                    category="Behavioral",
                    difficulty="easy",
                ),
                InterviewQuestion(
                    question="Describe a challenging project you worked on and how you overcame obstacles.",
                    category="Behavioral",
                    difficulty="medium",
                ),
            ]

        return InterviewReport(questions=questions)
