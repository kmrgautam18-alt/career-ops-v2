from datetime import date, datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

StatusStr = Annotated[
    str,
    Field(
        min_length=3,
        max_length=30,
        strip_whitespace=True,
        description="Application status",
        examples=["Applied"],
    ),
]


class ApplicationCreate(BaseModel):
    job_id: int
    applied_date: date
    status: StatusStr = "Applied"
    notes: str | None = None


class ApplicationUpdate(BaseModel):
    status: StatusStr | None = None
    applied_date: date | None = None
    notes: str | None = None


class ApplicationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    job_id: int
    status: str
    applied_date: date
    notes: str | None
    created_at: datetime
    updated_at: datetime
