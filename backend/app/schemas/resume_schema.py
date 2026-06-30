from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ResumeCreate(BaseModel):
    title: str


class ResumeUpdate(BaseModel):
    title: str


class ResumeResponse(BaseModel):
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

    model_config = ConfigDict(
        from_attributes=True,
    )