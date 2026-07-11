from __future__ import annotations

from dataclasses import dataclass, field

from backend.app.services.education_extractor.education_models import (
    EducationRecord,
)


@dataclass(slots=True)
class ValidationIssue:
    """
    Represents a validation error or warning.
    """

    field: str
    message: str


@dataclass(slots=True)
class ValidationResult:
    """
    Validation result for one education record.
    """

    is_valid: bool

    errors: list[ValidationIssue] = field(
        default_factory=list,
    )

    warnings: list[ValidationIssue] = field(
        default_factory=list,
    )


def validate_education(
    record: EducationRecord,
) -> ValidationResult:
    """
    Validate one EducationRecord.
    """

    errors: list[ValidationIssue] = []

    warnings: list[ValidationIssue] = []

    # ---------------------------------------
    # Required
    # ---------------------------------------

    if not record.degree:

        errors.append(
            ValidationIssue(
                field="degree",
                message="Degree is missing.",
            )
        )

    # ---------------------------------------
    # Recommended
    # ---------------------------------------

    if not record.specialization:

        warnings.append(
            ValidationIssue(
                field="specialization",
                message="Specialization is missing.",
            )
        )

    if not record.institution:

        warnings.append(
            ValidationIssue(
                field="institution",
                message="Institution is missing.",
            )
        )

    # ---------------------------------------
    # Date validation
    # ---------------------------------------

    if (
        record.start_date
        and record.end_date
        and record.start_date > record.end_date
    ):

        errors.append(
            ValidationIssue(
                field="date_range",
                message="Start date cannot be after end date.",
            )
        )

    # ---------------------------------------
    # Confidence validation
    # ---------------------------------------

    if not (
        0.0 <= record.confidence <= 1.0
    ):

        errors.append(
            ValidationIssue(
                field="confidence",
                message="Confidence must be between 0.0 and 1.0.",
            )
        )

    return ValidationResult(
        is_valid=not errors,
        errors=errors,
        warnings=warnings,
    )