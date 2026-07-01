from fastapi import UploadFile
from sqlalchemy.orm import Session

from backend.app.core.resume_status import ResumeStatus
from backend.app.exceptions.resume_exceptions import (
    InvalidResumeFileException,
)
from backend.app.repositories.resume_repository_sa import (
    create_resume,
)
from backend.app.schemas.common_schema import ApiResponse
from backend.app.schemas.resume_schema import ResumeResponse
from backend.app.utils.file_storage import (
    create_user_storage_directory,
    generate_uuid_filename,
    save_uploaded_file,
)
from backend.app.utils.file_validator import (
    validate_resume_file,
)


def upload_resume(
    db: Session,
    user,
    title: str,
    upload_file: UploadFile,
):
    """
    Upload a resume.

    Workflow
    --------
    1. Validate file
    2. Generate UUID filename
    3. Create user storage directory
    4. Save file
    5. Store metadata
    6. Return API response
    """

    # Validate uploaded file
    validate_resume_file(upload_file)

    filename = upload_file.filename

    if filename is None:
        raise InvalidResumeFileException()

    # Generate unique filename
    stored_filename = generate_uuid_filename(
        filename,
    )

    # Create user storage directory
    user_directory = create_user_storage_directory(
        user.id,
    )

    destination = user_directory / stored_filename

    # Save file to disk
    save_uploaded_file(
        upload_file,
        destination,
    )

    # Store metadata
    resume = create_resume(
        db=db,
        user_id=user.id,
        title=title,
        original_filename=filename,
        stored_filename=stored_filename,
        file_path=str(destination),
        file_size=destination.stat().st_size,
        mime_type=upload_file.content_type,
        upload_status=ResumeStatus.UPLOADED,
    )

    return ApiResponse(
        success=True,
        message="Resume uploaded successfully.",
        data=ResumeResponse.model_validate(
            resume,
        ),
    )