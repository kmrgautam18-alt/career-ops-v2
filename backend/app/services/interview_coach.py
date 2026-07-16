"""
Interview Coach AI — Real-time mock interview practice with AI feedback.
Uses AI Model Abstraction Layer (supports Gemini, OpenAI, Claude).
"""

from __future__ import annotations

import logging
from collections.abc import AsyncGenerator
from typing import Any

from backend.app.services.ai.models import get_model

logger = logging.getLogger(__name__)

COACH_SYSTEM_PROMPT = """You are an expert technical interview coach.
Your role is to:
1. Ask realistic interview questions based on the job role and company
2. Evaluate the user's answers constructively
3. Provide specific, actionable feedback
4. Suggest better ways to structure responses
5. Score answers on: technical accuracy, communication, structure, and relevance

Keep responses encouraging but honest. Focus on growth mindset."""

MOCK_INTERVIEW_PROMPT = """You are conducting a mock interview for a {job_title} position at {company}.
Difficulty level: {difficulty}
Focus areas: {focus_areas}

Interview type: {interview_type}

First, ask the candidate an appropriate interview question based on their experience level.
After they answer, provide feedback in JSON format:
{{
    "question": "the question you asked",
    "expected_answer_keywords": ["key1", "key2"],
    "score": 0-100,
    "strengths": ["strength1"],
    "improvements": ["improvement1"],
    "suggested_answer": "An ideal answer structure",
    "follow_up_question": "A follow-up to dig deeper"
}}

Start by asking the first question."""

FEEDBACK_PROMPT = """Analyze this interview answer for a {job_title} position at {company}.

Question: {question}
Candidate's Answer: {answer}

Return JSON with:
{{
    "technical_score": 0-100,
    "communication_score": 0-100,
    "structure_score": 0-100,
    "overall_score": 0-100,
    "strengths": ["strength1"],
    "areas_for_improvement": ["area1"],
    "suggested_improvement": "Detailed suggestion",
    "sample_answer": "How a strong answer would sound"
}}"""


async def start_interview(
    job_title: str,
    company: str,
    difficulty: str = "medium",
    focus_areas: str = "general",
    interview_type: str = "technical",
    provider: str | None = None,
) -> AsyncGenerator[str, None]:
    """Start a mock interview and get the first question."""
    model = get_model(provider)

    prompt = MOCK_INTERVIEW_PROMPT.format(
        job_title=job_title,
        company=company,
        difficulty=difficulty,
        focus_areas=focus_areas,
        interview_type=interview_type,
    )

    async for chunk in model.stream(prompt, COACH_SYSTEM_PROMPT):
        yield chunk


async def analyze_answer(
    question: str,
    answer: str,
    job_title: str,
    company: str,
    provider: str | None = None,
) -> dict[str, Any]:
    """Analyze a candidate's answer and return structured feedback."""
    model = get_model(provider)

    prompt = FEEDBACK_PROMPT.format(
        job_title=job_title,
        company=company,
        question=question,
        answer=answer,
    )

    return await model.generate_json(prompt)


async def generate_practice_plan(
    job_title: str,
    target_company: str,
    years_experience: int,
    weak_areas: list[str] | None = None,
    provider: str | None = None,
) -> dict[str, Any]:
    """Generate a personalized interview practice plan."""
    model = get_model(provider)

    weak_areas_str = ", ".join(weak_areas) if weak_areas else "none specified"
    prompt = f"""Create a 7-day interview preparation plan for a {job_title} position at {target_company}.
Years of experience: {years_experience}
Weak areas to focus on: {weak_areas_str}

Return JSON:
{{
    "overall_strategy": "Main approach recommendation",
    "daily_plan": [
        {{
            "day": 1,
            "focus": "Topic",
            "practice_questions": ["q1", "q2", "q3"],
            "resources": ["resource1"],
            "time_estimate_minutes": 30
        }}
    ],
    "key_topics_to_review": ["topic1"],
    "recommended_resources": [{{"name": "name", "url": "url"}}]
}}"""

    return await model.generate_json(prompt)
