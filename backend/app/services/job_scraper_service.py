"""
Job Scraper Service for Auto Job Application Engine.
Simulates scraping jobs from LinkedIn, Indeed, Google Jobs, and company career portals.
In production, this would integrate with real APIs (LinkedIn Ads API, Indeed Publisher API, etc.)
"""

from __future__ import annotations

import logging
import random
from typing import Any

from backend.app.schemas.auto_application_schema import ScrapedJobItem

logger = logging.getLogger(__name__)

# ── Mock Company Database ──────────────────────────────────────────────

MOCK_COMPANIES: list[dict[str, Any]] = [
    {"name": "Google", "career_url": "https://careers.google.com", "hr_email": "careers@google.com"},
    {"name": "Microsoft", "career_url": "https://careers.microsoft.com", "hr_email": "careers@microsoft.com"},
    {"name": "Amazon", "career_url": "https://amazon.jobs", "hr_email": "jobs@amazon.com"},
    {"name": "Meta", "career_url": "https://metacareers.com", "hr_email": "careers@meta.com"},
    {"name": "Apple", "career_url": "https://apple.com/careers", "hr_email": "careers@apple.com"},
    {"name": "Netflix", "career_url": "https://jobs.netflix.com", "hr_email": "jobs@netflix.com"},
    {"name": "Spotify", "career_url": "https://www.lifeatspotify.com/jobs", "hr_email": "jobs@spotify.com"},
    {"name": "Stripe", "career_url": "https://stripe.com/jobs", "hr_email": "jobs@stripe.com"},
    {"name": "Airbnb", "career_url": "https://careers.airbnb.com", "hr_email": "careers@airbnb.com"},
    {"name": "Uber", "career_url": "https://www.uber.com/us/en/careers", "hr_email": "careers@uber.com"},
    {"name": "Shopify", "career_url": "https://www.shopify.com/careers", "hr_email": "careers@shopify.com"},
    {"name": "Twilio", "career_url": "https://www.twilio.com/company/jobs", "hr_email": "jobs@twilio.com"},
    {"name": "Datadog", "career_url": "https://www.datadoghq.com/careers", "hr_email": "careers@datadoghq.com"},
    {"name": "Cloudflare", "career_url": "https://www.cloudflare.com/careers", "hr_email": "careers@cloudflare.com"},
    {"name": "GitHub", "career_url": "https://github.com/about/careers", "hr_email": "careers@github.com"},
    {"name": "Palantir", "career_url": "https://www.palantir.com/careers", "hr_email": "careers@palantir.com"},
    {"name": "Coinbase", "career_url": "https://www.coinbase.com/careers", "hr_email": "careers@coinbase.com"},
    {"name": "Square", "career_url": "https://squareup.com/us/en/careers", "hr_email": "careers@square.com"},
]

MOCK_JOB_TITLES_BY_CATEGORY: dict[str, list[str]] = {
    "software engineer": [
        "Senior Software Engineer", "Software Engineer II", "Software Engineer",
        "Backend Engineer", "Full Stack Engineer", "Frontend Engineer",
        "Staff Software Engineer", "Principal Engineer", "Lead Software Engineer",
    ],
    "data scientist": [
        "Data Scientist", "Senior Data Scientist", "ML Engineer",
        "Machine Learning Engineer", "Data Analyst", "Data Engineer",
    ],
    "devops": [
        "DevOps Engineer", "SRE Engineer", "Platform Engineer",
        "Cloud Engineer", "Infrastructure Engineer", "Site Reliability Engineer",
    ],
    "product manager": [
        "Product Manager", "Senior Product Manager", "Technical Product Manager",
        "Associate Product Manager", "Product Owner",
    ],
    "designer": [
        "UX Designer", "Product Designer", "UI Designer",
        "Senior Product Designer", "Design Lead", "Visual Designer",
    ],
}

# ── Scraping Functions ─────────────────────────────────────────────────


def _generate_mock_jobs(
    category_titles: list[str],
    count: int,
    source: str,
) -> list[ScrapedJobItem]:
    """Generate mock job listings for testing."""
    jobs: list[ScrapedJobItem] = []
    companies = random.sample(MOCK_COMPANIES, min(count * 2, len(MOCK_COMPANIES)))

    for i in range(count):
        if i >= len(companies):
            break
        company = companies[i]
        title = random.choice(category_titles)
        description = _generate_mock_description(title, company["name"])
        location = random.choice([
            "Remote", "San Francisco, CA", "New York, NY", "Seattle, WA",
            "Austin, TX", "Boston, MA", "Chicago, IL", "Denver, CO",
        ])
        url = (
            f"https://www.linkedin.com/jobs/view/{100000 + i}/"
            if source == "linkedin"
            else f"https://www.indeed.com/viewjob?jk={random.randint(10000, 99999)}"
            if source == "indeed"
            else f"{company['career_url']}/jobs/{random.randint(1000, 9999)}/"
        )

        jobs.append(ScrapedJobItem(
            company=company["name"],
            title=title,
            url=url,
            description=description,
            location=location,
        ))

    return jobs


def _generate_mock_description(title: str, company: str) -> str:
    """Generate a realistic mock job description."""
    responsibilities = random.sample([
        "Design and implement scalable solutions",
        "Collaborate with cross-functional teams",
        "Write clean, well-tested code",
        "Participate in code reviews",
        "Mentor junior team members",
        "Drive technical decision-making",
        "Build and maintain API integrations",
        "Optimize system performance",
        "Contribute to architectural design",
        "Develop and maintain documentation",
    ], 3)

    requirements = random.sample([
        "Strong problem-solving skills",
        "Excellent communication skills",
        "Experience with distributed systems",
        "Proven track record of delivering results",
        "Strong understanding of data structures and algorithms",
        "Experience with Agile methodologies",
        "Ability to work independently",
        "Experience with cloud platforms (AWS/GCP/Azure)",
    ], 3)

    return (
        f"**Position:** {title}\n"
        f"**Company:** {company}\n\n"
        f"**About the Role:**\n"
        f"We are looking for a talented {title} to join our growing team at {company}. "
        f"In this role, you will work on impactful projects that reach millions of users worldwide.\n\n"
        f"**Responsibilities:**\n"
        + "\n".join(f"• {r}" for r in responsibilities) +
        "\n\n**Requirements:**\n"
        + "\n".join(f"• {r}" for r in requirements) +
        f"\n\n**Nice to Have:**\n"
        f"• Experience with our tech stack\n"
        f"• Open source contributions\n"
        f"• Previous experience at a high-growth company\n\n"
        f"{company} is an equal opportunity employer. We celebrate diversity and are "
        f"committed to creating an inclusive environment for all employees."
    )


# ── Public API ─────────────────────────────────────────────────────────


def scrape_linkedin(query: str, location: str | None = None, max_results: int = 10) -> list[ScrapedJobItem]:
    """
    Simulate scraping jobs from LinkedIn.
    In production, this would use the LinkedIn Jobs API or a scraping service.

    Args:
        query: Job search query (e.g. "Software Engineer")
        location: Optional location filter
        max_results: Maximum number of jobs to return

    Returns:
        List of scraped job items
    """
    logger.info("Scraping LinkedIn for '%s' (max: %d)", query, max_results)
    category = _find_category(query)
    titles = MOCK_JOB_TITLES_BY_CATEGORY.get(category, MOCK_JOB_TITLES_BY_CATEGORY["software engineer"])
    jobs = _generate_mock_jobs(titles, min(max_results, 10), "linkedin")

    if location:
        # Filter to matching locations
        jobs = [j for j in jobs if location.lower() in j.location.lower()] if jobs else jobs

    logger.info("Found %d jobs on LinkedIn for '%s'", len(jobs), query)
    return jobs


def scrape_indeed(query: str, location: str | None = None, max_results: int = 10) -> list[ScrapedJobItem]:
    """
    Simulate scraping jobs from Indeed.
    In production, this would use the Indeed Publisher API.

    Args:
        query: Job search query
        location: Optional location filter
        max_results: Maximum number of jobs to return

    Returns:
        List of scraped job items
    """
    logger.info("Scraping Indeed for '%s' (max: %d)", query, max_results)
    category = _find_category(query)
    titles = MOCK_JOB_TITLES_BY_CATEGORY.get(category, MOCK_JOB_TITLES_BY_CATEGORY["software engineer"])
    jobs = _generate_mock_jobs(titles, min(max_results, 10), "indeed")

    if location:
        jobs = [j for j in jobs if location.lower() in j.location.lower()] if jobs else jobs

    logger.info("Found %d jobs on Indeed for '%s'", len(jobs), query)
    return jobs


def scrape_company_career_page(
    company_name: str | None = None,
    query: str = "",
    max_results: int = 10,
) -> list[ScrapedJobItem]:
    """
    Simulate scraping a company's career page.
    In production, this would scrape the actual career page or use a provider.

    Args:
        company_name: Optional specific company to scrape
        query: Job search query
        max_results: Maximum number of jobs

    Returns:
        List of scraped job items
    """
    logger.info("Scraping career page (company: %s, query: '%s')", company_name or "any", query)

    category = _find_category(query)
    titles = MOCK_JOB_TITLES_BY_CATEGORY.get(category, MOCK_JOB_TITLES_BY_CATEGORY["software engineer"])

    if company_name:
        # Specific company
        matched = [c for c in MOCK_COMPANIES if company_name.lower() in c["name"].lower()]
        if not matched:
            logger.info("Company '%s' not found in mock database", company_name)
            return []
        companies = matched[:max_results]
    else:
        companies = MOCK_COMPANIES[:max_results]

    jobs: list[ScrapedJobItem] = []
    for company in companies:
        title = random.choice(titles)
        description = _generate_mock_description(title, company["name"])
        jobs.append(ScrapedJobItem(
            company=company["name"],
            title=title,
            url=f"{company['career_url']}/jobs/{random.randint(1000, 9999)}/",
            description=description,
            location=random.choice(["Remote", "San Francisco, CA", "New York, NY"]),
        ))

    logger.info("Found %d jobs on career pages", len(jobs))
    return jobs


def scrape_jobs(
    source: str,
    query: str,
    location: str | None = None,
    max_results: int = 10,
) -> list[ScrapedJobItem]:
    """
    Scrape jobs from the specified source.

    Args:
        source: 'linkedin', 'indeed', 'company_career', or 'all'
        query: Job search query
        location: Optional location filter
        max_results: Maximum results per source

    Returns:
        Combined list of scraped jobs
    """
    if source == "linkedin":
        return scrape_linkedin(query, location, max_results)
    elif source == "indeed":
        return scrape_indeed(query, location, max_results)
    elif source == "company_career":
        return scrape_company_career_page(None, query, max_results)
    elif source == "all":
        all_jobs = []
        all_jobs.extend(scrape_linkedin(query, location, max_results // 2))
        all_jobs.extend(scrape_indeed(query, location, max_results // 2))
        all_jobs.extend(scrape_company_career_page(None, query, max_results // 2))
        return all_jobs[:max_results]
    else:
        logger.warning("Unknown source: %s", source)
        return []


def _find_category(query: str) -> str:
    """Determine the job category from a search query."""
    query_lower = query.lower()
    if any(word in query_lower for word in ["engineer", "developer", "software", "backend", "frontend", "full stack"]):
        return "software engineer"
    if any(word in query_lower for word in ["data", "ml", "machine learning", "scientist", "analyst"]):
        return "data scientist"
    if any(word in query_lower for word in ["devops", "sre", "platform", "cloud", "infrastructure"]):
        return "devops"
    if any(word in query_lower for word in ["product", "manager"]):
        return "product manager"
    if any(word in query_lower for word in ["designer", "ux", "ui", "design"]):
        return "designer"
    return "software engineer"
