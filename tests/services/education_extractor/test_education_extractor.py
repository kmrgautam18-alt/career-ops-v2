from datetime import date

from backend.app.services.education_extractor.degree_detector import (
    detect_degrees,
)
from backend.app.services.education_extractor.education_builder import (
    build_education,
)
from backend.app.services.education_extractor.education_models import (
    EducationRecord,
)
from backend.app.services.education_extractor.education_validator import (
    validate_education,
)
from backend.app.services.education_extractor.extractor import (
    extract_education,
)
from backend.app.services.education_extractor.specialization_detector import (
    detect_specializations,
)

# ==========================================================
# Degree Detector
# ==========================================================


def test_degree_detector():

    assert detect_degrees(
        "Bachelor of Technology"
    ) == [
        "Bachelor of Technology",
    ]


def test_unknown_degree():

    assert detect_degrees(
        "Unknown Degree"
    ) == []


# ==========================================================
# Specialization Detector
# ==========================================================


def test_specialization_detector():

    assert detect_specializations(
        "Computer Science and Engineering"
    ) == [
        "Computer Science and Engineering",
    ]


def test_unknown_specialization():

    assert detect_specializations(
        "Unknown Specialization"
    ) == []


# ==========================================================
# Builder
# ==========================================================


def test_build_education():

    record = build_education(
        """
Bachelor of Technology
Computer Science and Engineering
"""
    )

    assert record.degree == "Bachelor of Technology"

    assert (
        record.specialization
        == "Computer Science and Engineering"
    )


# ==========================================================
# Extractor
# ==========================================================


def test_extract_education():

    records = extract_education(
        """
Bachelor of Technology
Computer Science and Engineering

Master of Business Administration
Finance
"""
    )

    assert len(records) == 2

    assert (
        records[0].degree
        == "Bachelor of Technology"
    )

    assert (
        records[1].degree
        == "Master of Business Administration"
    )


def test_empty_education():

    assert extract_education("") == []


# ==========================================================
# Validator
# ==========================================================


def test_validator_valid_record():

    record = EducationRecord(
        degree="Bachelor of Technology",
        specialization="Computer Science",
    )

    result = validate_education(
        record,
    )

    assert result.is_valid

    assert len(result.errors) == 0


def test_validator_invalid_record():

    record = EducationRecord(
        start_date=date(2025, 1, 1),
        end_date=date(2024, 1, 1),
        confidence=2.0,
    )

    result = validate_education(
        record,
    )

    assert not result.is_valid

    assert len(result.errors) == 3

    assert len(result.warnings) == 2


# ==========================================================
# End-to-End
# ==========================================================


def test_end_to_end_education():

    records = extract_education(
        """
Bachelor of Technology
Computer Science and Engineering

Master of Business Administration
Finance
"""
    )

    assert len(records) == 2

    first = records[0]

    assert (
        first.degree
        == "Bachelor of Technology"
    )

    assert (
        first.specialization
        == "Computer Science and Engineering"
    )