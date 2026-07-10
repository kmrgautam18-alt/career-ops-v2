from __future__ import annotations

from dataclasses import dataclass

from backend.app.services.experience_extractor.experience_models import (
    ExperienceRecord,
)


@dataclass(slots=True)
class ValidationIssue:
    """
    Represents one validation issue.

    Future
    -------
    - error_code
    - severity
    - suggestion
    """

    field: str

    message: str


@dataclass(slots=True)
class ValidationResult:
    """
    Validation result returned by validator.

    Future
    -------
    - auto_fix_available
    - repaired_record
    """

    is_valid: bool

    errors: list[ValidationIssue]

    warnings: list[ValidationIssue]


def validate_experience(
    record: ExperienceRecord,
) -> ValidationResult:
    """
    Validate a parsed experience record.
    """

    errors: list[ValidationIssue] = []

    warnings: list[ValidationIssue] = []

    # ----------------------------------------------------
    # Company
    # ----------------------------------------------------

    if not record.company:

        errors.append(
            ValidationIssue(
                field="company",
                message="Company is missing.",
            )
        )

    # ----------------------------------------------------
    # Designation
    # ----------------------------------------------------

    if not record.designation:

        errors.append(
            ValidationIssue(
                field="designation",
                message="Designation is missing.",
            )
        )

    # ----------------------------------------------------
    # Date validation
    # ----------------------------------------------------

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

    # ----------------------------------------------------
    # Current Job validation
    # ----------------------------------------------------

    if (
        record.currently_working
        and record.end_date is not None
    ):

        errors.append(
            ValidationIssue(
                field="currently_working",
                message="Current job cannot have an end date.",
            )
        )

    # ----------------------------------------------------
    # Duration validation
    # ----------------------------------------------------

    if (
        record.duration_months is not None
        and record.duration_months < 0
    ):

        errors.append(
            ValidationIssue(
                field="duration_months",
                message="Duration cannot be negative.",
            )
        )

    # ----------------------------------------------------
    # Confidence validation
    # ----------------------------------------------------

    if not (
        0.0 <= record.confidence <= 1.0
    ):

        errors.append(
            ValidationIssue(
                field="confidence",
                message="Confidence must be between 0.0 and 1.0.",
            )
        )

    # ----------------------------------------------------
    # Description cleanup
    # ----------------------------------------------------

    if record.description:

        record.description = record.description.strip()

    else:

        warnings.append(
            ValidationIssue(
                field="description",
                message="Description is missing.",
            )
        )

    # ----------------------------------------------------
    # Location warning
    # ----------------------------------------------------

    if not record.location:

        warnings.append(
            ValidationIssue(
                field="location",
                message="Location is missing.",
            )
        )

    # ----------------------------------------------------
    # Employment Type warning
    # ----------------------------------------------------

    if not record.employment_type:

        warnings.append(
            ValidationIssue(
                field="employment_type",
                message="Employment type is missing.",
            )
        )

    return ValidationResult(
        is_valid=len(errors) == 0,
        errors=errors,
        warnings=warnings,
    )