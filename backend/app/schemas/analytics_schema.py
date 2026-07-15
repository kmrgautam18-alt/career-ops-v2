from datetime import date
from pydantic import BaseModel


class AnalyticsOverview(BaseModel):
    total_jobs: int = 0
    total_applications: int = 0
    applications_by_status: dict[str, int] = {}
    interviews_count: int = 0
    offers_count: int = 0
    acceptance_rate: float = 0.0
    ats_score_avg: float = 0.0


class MonthlyStats(BaseModel):
    month: str
    applications: int = 0
    interviews: int = 0
    offers: int = 0


class SkillAnalytics(BaseModel):
    skill: str
    count: int
    category: str = ""


class ApplicationTrend(BaseModel):
    date: str
    count: int
