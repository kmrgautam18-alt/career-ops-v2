"""
File storage utility.

Provides reusable helper functions for file storage operations.
"""

import shutil
from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from backend.app.core.file_constants import (
    RESUME_STORAGE_DIR,
)


def generate_uuid_filename(
    original_filename: str,
) -> str:
    """
    Generate a unique filename while preserving the extension.
    """

    extension = Path(original_filename).suffix.lower()

    return f"{uuid4()}{extension}"


def create_user_storage_directory(
    user_id: int,
) -> Path:
    """
    Create (if required) and return the user's storage directory.
    """

    directory = RESUME_STORAGE_DIR / str(user_id)

    directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    return directory


def save_uploaded_file(
    upload_file: UploadFile,
    destination: Path,
) -> None:
    """
    Save an uploaded file to disk.
    """

    with destination.open("wb") as buffer:
        shutil.copyfileobj(
            upload_file.file,
            buffer,
        )


def delete_uploaded_file(
    file_path: Path,
) -> bool:
    """
    Delete a stored file if it exists.

    Returns:
        True if the file was deleted.
        False if the file did not exist.
    """

    if not file_path.exists():
        return False

    file_path.unlink()

    return True


def file_exists(
    file_path: Path,
) -> bool:
    """
    Check whether a file exists.
    """

    return file_path.exists()
