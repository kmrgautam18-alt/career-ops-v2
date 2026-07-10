from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(slots=True)
class DurationResult:
    """
    Represents calculated work experience.
    """

    years: int
    months: int
    total_months: int


def calculate_duration(
    start_date: date,
    end_date: date,
) -> DurationResult:
    """
    Calculate work experience between two dates.
    """

    if end_date < start_date:
        raise ValueError(
            "end_date cannot be earlier than start_date"
        )

    total_months = (
        (end_date.year - start_date.year) * 12
        + (end_date.month - start_date.month)
    )

    years = total_months // 12
    months = total_months % 12

    return DurationResult(
        years=years,
        months=months,
        total_months=total_months,
    )