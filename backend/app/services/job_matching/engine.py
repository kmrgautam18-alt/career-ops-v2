from backend.app.services.job_matching.matchers.skill_matcher import SkillMatcher
from backend.app.services.job_matching.matchers.experience_matcher import ExperienceMatcher
from backend.app.services.job_matching.matchers.education_matcher import EducationMatcher
from backend.app.services.job_matching.matchers.certification_matcher import CertificationMatcher
from backend.app.services.job_matching.matchers.location_matcher import LocationMatcher
from backend.app.services.job_matching.matchers.keyword_matcher import KeywordMatcher

from backend.app.services.job_matching.score_calculator import ScoreCalculator
from backend.app.services.job_matching.recommendation_engine import RecommendationEngine
from backend.app.services.job_matching.explainability import ExplainabilityEngine

from backend.app.services.job_matching.models import MatchResult


class JobMatchingEngine:
    @staticmethod
    def match(
        *,
        resume_skills: list[str],
        job_skills: list[str],
        candidate_years: float,
        required_years: float,
        candidate_degree: str,
        required_degree: str,
        candidate_certifications: list[str],
        required_certifications: list[str],
        candidate_location: str,
        job_location: str,
        remote: bool,
        resume_text: str,
        job_text: str,
    ) -> MatchResult:

        skill = SkillMatcher.match(
            resume_skills,
            job_skills,
        )

        experience = ExperienceMatcher.match(
            candidate_years,
            required_years,
        )

        education = EducationMatcher.match(
            candidate_degree,
            required_degree,
        )

        certification = CertificationMatcher.match(
            candidate_certifications,
            required_certifications,
        )

        location = LocationMatcher.match(
            candidate_location,
            job_location,
            remote,
        )

        keyword = KeywordMatcher.match(
            resume_text,
            job_text,
        )

        overall = ScoreCalculator.calculate(
    skill=skill.score,
    experience=experience.score,
    education=education.score,
    certification=certification.score,
    keyword=keyword.score,
    location=location.score,
)

        recommendations = RecommendationEngine.generate(
            skill.missing,
            overall,
        )

        strengths = skill.matched

        weaknesses = skill.missing

        return MatchResult(
            overall_score=overall,
            skill=skill,
            experience=experience,
            education=education,
            certification=certification,
            keyword=keyword,
            location=location,
            classification="Strong Match",
            strengths=strengths,
            weaknesses=weaknesses,
            recommendations=recommendations,
        )