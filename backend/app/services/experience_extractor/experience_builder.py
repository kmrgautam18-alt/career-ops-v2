from __future__ import annotations

import re
from datetime import date

from backend.app.services.experience_extractor.company_detector import (
    detect_companies,
)
from backend.app.services.experience_extractor.confidence_engine import (
    calculate_confidence,
)
from backend.app.services.experience_extractor.current_job_detector import (
    is_current_job,
)
from backend.app.services.experience_extractor.date_parser import (
    parse_date,
)
from backend.app.services.experience_extractor.description_extractor import (
    extract_description,
)
from backend.app.services.experience_extractor.designation_detector import (
    detect_designations,
)
from backend.app.services.experience_extractor.duration_calculator import (
    calculate_duration,
)
from backend.app.services.experience_extractor.employment_type_detector import (
    detect_employment_type,
)
from backend.app.services.experience_extractor.experience_models import (
    ExperienceRecord,
)
from backend.app.services.experience_extractor.location_detector import (
    detect_locations,
)


DATE_RANGE_PATTERN = re.compile(
    r"(?P<start>.+?)\s*[-–]\s*(?P<end>.+)",
    re.IGNORECASE,
)


def _first_or_none(
    values: list[str],
) -> str | None:

    return values[0] if values else None


def _extract_date_range(
    block: str,
) -> tuple[
    date | None,
    date | None,
    bool,
]:

    for line in block.splitlines():

        line = line.strip()

        if not line:
            continue

        match = DATE_RANGE_PATTERN.search(line)

        if not match:
            continue

        start_text = match.group("start").strip()
        end_text = match.group("end").strip()

        start_date = parse_date(start_text)

        if start_date is None:
            continue

        end_date = parse_date(end_text)

        currently_working = is_current_job(
            end_text,
        )

        return (
            start_date,
            end_date,
            currently_working,
        )

    return (
        None,
        None,
        False,
    )


def build_experience(
    block: str,
) -> ExperienceRecord:
    """
    Build one ExperienceRecord from one
    resume experience block.
    """

    companies = detect_companies(block)

    designations = detect_designations(block)

    locations = detect_locations(block)

    employment_type = detect_employment_type(block)

    description = extract_description(block)

    (
        start_date,
        end_date,
        currently_working,
    ) = _extract_date_range(block)

    duration_months = None

    if start_date:

        duration = calculate_duration(
            start_date,
            end_date or date.today(),
        )

        duration_months = duration.total_months

    record = ExperienceRecord(
        company=_first_or_none(companies),
        designation=_first_or_none(designations),
        employment_type=(
            employment_type.value
            if employment_type
            else None
        ),
        location=_first_or_none(locations),
        start_date=start_date,
        end_date=end_date,
        currently_working=currently_working,
        duration_months=duration_months,
        description=description,
    )

    record.confidence = calculate_confidence(
        record,
    )

    return record