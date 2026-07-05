from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

ResumeTitle = Annotated[
    str,
    Field(
        min_length=2,
        max_length=200,
        strip_whitespace=True,
        description="Resume title",
        examples=["Senior DevOps Resume"],
    ),
]


class ResumeCreate(BaseModel):
    title: ResumeTitle


class ResumeUpdate(BaseModel):
    title: ResumeTitle


class ResumeRename(BaseModel):
    title: ResumeTitle


class ResumeResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    user_id: int

    title: str

    original_filename: str
    stored_filename: str

    file_path: str

    file_size: int

    mime_type: str

    upload_status: str

    created_at: datetime
    updated_at: datetime
