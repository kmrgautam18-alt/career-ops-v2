from __future__ import annotations

from datetime import date

from backend.app.services.experience_extractor.company_detector import (
    detect_companies,
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
from backend.app.services.experience_extractor.location_detector import (
    detect_locations,
)


# ============================================================
# Company Detector
# ============================================================


def test_company_detector():

    text = """
    Microsoft
    Senior DevOps Engineer
    """

    companies = detect_companies(text)

    assert "Microsoft" in companies


def test_unknown_company():

    companies = detect_companies(
        "Random Unknown Organization"
    )

    assert companies == []


# ============================================================
# Designation Detector
# ============================================================


def test_designation_detector():

    titles = detect_designations(
        "Senior DevOps Engineer"
    )

    assert "Senior DevOps Engineer" in titles


def test_unknown_designation():

    titles = detect_designations(
        "Random Hero"
    )

    assert titles == []


# ============================================================
# Location Detector
# ============================================================


def test_location_detector():

    locations = detect_locations(
        "Hyderabad India"
    )

    assert "Hyderabad" in locations


# ============================================================
# Employment Type
# ============================================================


def test_employment_type():

    employment = detect_employment_type(
        "Full-Time"
    )

    assert employment.value == "Full Time"


# ============================================================
# Date Parser
# ============================================================


def test_parse_month_year():

    assert parse_date(
        "Jan 2022"
    ) == date(
        2022,
        1,
        1,
    )


def test_parse_year():

    assert parse_date(
        "2022"
    ) == date(
        2022,
        1,
        1,
    )


def test_parse_present():

    assert parse_date(
        "Present"
    ) is None


def test_parse_empty():

    assert parse_date(
        ""
    ) is None


# ============================================================
# Duration
# ============================================================


def test_duration():

    result = calculate_duration(
        date(
            2022,
            1,
            1,
        ),
        date(
            2024,
            3,
            1,
        ),
    )

    assert result.total_months == 26

    assert result.years == 2

    assert result.months == 2


# ============================================================
# Description
# ============================================================


def test_description():

    text = """
    Worked on Azure DevOps.

    Managed Kubernetes.

    Implemented CI/CD.
    """

    description = extract_description(
        text,
    )

    assert "Azure" in description

    assert "Kubernetes" in description

    assert "CI/CD" in description

# ============================================================
# Confidence Engine
# ============================================================

from backend.app.services.experience_extractor.confidence_engine import (
    calculate_confidence,
)
from backend.app.services.experience_extractor.experience_models import (
    ExperienceRecord,
)


def test_confidence_engine():

    record = ExperienceRecord(
        company="Microsoft",
        designation="Senior DevOps Engineer",
        employment_type="Full Time",
        location="Hyderabad",
        start_date=date(2022, 1, 1),
        duration_months=24,
        description="Worked on Azure",
    )

    assert calculate_confidence(record) == 1.0


def test_partial_confidence():

    record = ExperienceRecord(
        company="Microsoft",
        start_date=date(2022, 1, 1),
    )

    assert calculate_confidence(record) == 0.4 

# ============================================================
# Experience Builder
# ============================================================

from backend.app.services.experience_extractor.experience_builder import (
    build_experience,
)


def test_build_experience():

    text = """
    Microsoft
    Senior DevOps Engineer
    Hyderabad
    Full-Time
    Jan 2022 - Present

    Worked on Azure DevOps.
    """

    record = build_experience(text)

    assert record.company == "Microsoft"

    assert record.designation == "Senior DevOps Engineer"

    assert record.location == "Hyderabad"

    assert record.employment_type == "Full Time"

    assert record.currently_working is True

    assert record.start_date == date(
        2022,
        1,
        1,
    )

    assert record.duration_months is not None

    assert record.confidence == 1.0

    assert "Azure" in record.description

def test_build_experience_without_description():

    text = """
    Microsoft
    Senior DevOps Engineer
    Hyderabad
    Full-Time
    Jan 2022 - Present
    """

    record = build_experience(
        text,
    )

    assert record.description is None

    assert record.company == "Microsoft"

    assert record.designation == "Senior DevOps Engineer"  

# ============================================================
# Experience Validator
# ============================================================

from backend.app.services.experience_extractor.experience_validator import (
    validate_experience,
)


def test_validator_valid_record():

    record = build_experience(
        """
        Microsoft
        Senior DevOps Engineer
        Hyderabad
        Full-Time
        Jan 2022 - Present

        Worked on Azure DevOps.
        """
    )

    result = validate_experience(record)

    assert result.is_valid is True

    assert result.errors == []

    assert result.warnings == []


def test_validator_invalid_record():

    record = ExperienceRecord(
        confidence=2.0,
    )

    result = validate_experience(record)

    assert result.is_valid is False

    error_fields = {
        issue.field
        for issue in result.errors
    }

    assert "company" in error_fields

    assert "designation" in error_fields

    assert "confidence" in error_fields

    warning_fields = {
        issue.field
        for issue in result.warnings
    }

    assert "description" in warning_fields

    assert "location" in warning_fields

    assert "employment_type" in warning_fields

def test_validator_date_range():

    record = ExperienceRecord(
        company="Microsoft",
        designation="DevOps Engineer",
        start_date=date(
            2025,
            1,
            1,
        ),
        end_date=date(
            2024,
            1,
            1,
        ),
    )

    result = validate_experience(
        record,
    )

    assert result.is_valid is False

    assert any(
        issue.field == "date_range"
        for issue in result.errors
    )

from backend.app.services.experience_extractor.extractor import (
    extract_experiences,
)

# ============================================================
# End-to-End Experience Extraction
# ============================================================

def test_single_experience_resume():

    resume = """
    Microsoft
    Senior DevOps Engineer
    Hyderabad
    Full-Time
    Jan 2022 - Present

    Worked on Azure DevOps.
    """

    records = extract_experiences(resume)

    assert len(records) == 1

    record = records[0]

    assert record.company == "Microsoft"

    assert record.designation == "Senior DevOps Engineer"

    assert record.currently_working is True

    assert record.location == "Hyderabad"

def test_multiple_experiences():

    resume = """
    Microsoft
    Senior DevOps Engineer
    Hyderabad
    Jan 2022 - Present

    Worked on Azure.

    TCS
    System Engineer
    Bangalore
    Jun 2019 - Dec 2021

    Worked on Linux.
    """

    records = extract_experiences(resume)

    assert len(records) == 2

    assert records[0].company == "Microsoft"

    assert records[1].company == "TCS"

    assert records[1].designation == "System Engineer"

def test_empty_resume():

    records = extract_experiences("")

    assert records == []

def test_current_job_detection():

    resume = """
    Microsoft
    DevOps Engineer
    Jan 2023 - Present
    """

    records = extract_experiences(resume)

    assert len(records) == 1

    assert records[0].currently_working is True          