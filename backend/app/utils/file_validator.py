"""
File validation utility.

Provides reusable validation functions for uploaded files.
"""

from pathlib import Path

from fastapi import UploadFile

from backend.app.core.file_constants import (
    ALLOWED_RESUME_EXTENSIONS,
    ALLOWED_RESUME_TYPES,
    MAX_RESUME_SIZE_BYTES,
)

from backend.app.exceptions.resume_exceptions import (
    InvalidResumeFileException,
    UnsupportedResumeTypeException,
    ResumeTooLargeException,
)


def validate_file_extension(
    upload_file: UploadFile,
) -> None:
    """
    Validate file extension.
    """

    extension = Path(upload_file.filename).suffix.lower()

    if extension not in ALLOWED_RESUME_EXTENSIONS:
        raise UnsupportedResumeTypeException()


def validate_mime_type(
    upload_file: UploadFile,
) -> None:
    """
    Validate MIME type.
    """

    if upload_file.content_type not in ALLOWED_RESUME_TYPES:
        raise UnsupportedResumeTypeException()


def validate_file_size(
    upload_file: UploadFile,
) -> None:
    """
    Validate uploaded file size.
    """

    upload_file.file.seek(0, 2)
    file_size = upload_file.file.tell()
    upload_file.file.seek(0)

    if file_size > MAX_RESUME_SIZE_BYTES:
        raise ResumeTooLargeException()


def validate_resume_file(
    upload_file: UploadFile,
) -> None:
    """
    Perform all resume file validations.
    """

    if not upload_file.filename:
        raise InvalidResumeFileException()

    validate_file_extension(upload_file)
    validate_mime_type(upload_file)
    validate_file_size(upload_file)