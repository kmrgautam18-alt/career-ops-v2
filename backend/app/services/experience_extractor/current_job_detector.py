from __future__ import annotations

from backend.app.services.experience_extractor.utils import (
    is_present_text,
)


def is_current_job(
    end_date_text: str,
) -> bool:
    """
    Detect whether an experience is the user's
    current job.

    Current implementation
    ----------------------
    - keyword based

    Future
    -------
    - Resume context
    - Timeline reasoning
    - LLM verification
    """

    return is_present_text(end_date_text)