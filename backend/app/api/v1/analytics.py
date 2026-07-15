"""
Module 14 — Analytics (Charts, Trends, Success Rate, Skill Analytics)
"""
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends

from backend.app.database.dependencies import get_db
from backend.app.models import Application, Job
from backend.app.schemas.analytics_schema import AnalyticsOverview, MonthlyStats, SkillAnalytics
from backend.app.security.dependencies import get_current_active_user
from sqlalchemy.orm import Session
from sqlalchemy import func, extract

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/overview")
def get_analytics_overview(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    total_jobs = db.query(Job).filter(Job.id.isnot(None)).count()
    total_apps = db.query(Application).filter(Application.id.isnot(None)).count()
    interviews = db.query(Application).filter(Application.status == "interview").count()
    offers = db.query(Application).filter(Application.status == "offer").count()
    accepted = db.query(Application).filter(Application.status == "accepted").count()

    statuses = db.query(Application.status, func.count(Application.id)).group_by(Application.status).all()
    by_status = {s: c for s, c in statuses}

    total_decided = offers + accepted
    acceptance_rate = (accepted / total_decided * 100) if total_decided > 0 else 0.0

    return {
        "success": True,
        "data": AnalyticsOverview(
            total_jobs=total_jobs,
            total_applications=total_apps,
            applications_by_status=by_status,
            interviews_count=interviews,
            offers_count=offers,
            acceptance_rate=round(acceptance_rate, 1),
        ).model_dump(),
    }


@router.get("/monthly")
def get_monthly_stats(
    months: int = 6,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    now = datetime.utcnow()
    stats = []
    for i in range(months - 1, -1, -1):
        month_start = datetime(now.year, now.month, 1) - timedelta(days=30 * i)
        month_end = datetime(now.year, now.month, 1) - timedelta(days=30 * (i - 1)) if i > 0 else now
        apps = db.query(Application).filter(
            Application.created_at >= month_start,
            Application.created_at < month_end,
        ).count()
        interviews_count = db.query(Application).filter(
            Application.created_at >= month_start,
            Application.created_at < month_end,
            Application.status == "interview",
        ).count()
        offers_count = db.query(Application).filter(
            Application.created_at >= month_start,
            Application.created_at < month_end,
            Application.status == "offer",
        ).count()
        stats.append(MonthlyStats(
            month=month_start.strftime("%Y-%m"),
            applications=apps,
            interviews=interviews_count,
            offers=offers_count,
        ))
    return {"success": True, "data": [s.model_dump() for s in stats]}


@router.get("/skills")
def get_skill_analytics(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    from backend.app.models.resume_skill import ResumeSkill
    skills = db.query(
        ResumeSkill.skill_name,
        func.count(ResumeSkill.id).label("count"),
        ResumeSkill.category,
    ).group_by(ResumeSkill.skill_name).order_by(func.count(ResumeSkill.id).desc()).limit(20).all()
    return {
        "success": True,
        "data": [SkillAnalytics(skill=s[0], count=s[1], category=s[2] or "").model_dump() for s in skills],
    }


@router.get("/applications-trend")
def get_application_trend(
    days: int = 30,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    from collections import Counter
    from datetime import date, timedelta as td
    start = date.today() - td(days=days)
    apps = db.query(Application.created_at).filter(
        Application.created_at >= start,
    ).all()
    counts = Counter(a.created_at.strftime("%Y-%m-%d") for a in apps if a.created_at)
    trends = []
    for i in range(days):
        d = (start + td(days=i)).isoformat()
        trends.append({"date": d, "count": counts.get(d, 0)})
    return {"success": True, "data": trends}
