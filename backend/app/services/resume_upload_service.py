from dataclasses import asdict
from datetime import datetime
import logging

from fastapi import UploadFile
from sqlalchemy.orm import Session

from backend.app.core.resume_status import ResumeStatus
from backend.app.exceptions.resume_exceptions import (
    InvalidResumeFileException,
)
from backend.app.repositories.resume_experience_repository import (
    ResumeExperienceRepository,
)
from backend.app.repositories.resume_repository_sa import (
    create_resume,
    update_resume,
)
from backend.app.repositories.resume_skill_repository import (
    ResumeSkillRepository,
)
from backend.app.schemas.common_schema import ApiResponse
from backend.app.schemas.resume_schema import ResumeResponse
from backend.app.services.resume_information_extractor import (
    extract_profile,
)
from backend.app.services.resume_parser_service import (
    parse_resume,
)
from backend.app.services.skill_extractor.skill_builder import (
    build_skills,
)
from backend.app.utils.file_storage import (
    create_user_storage_directory,
    generate_uuid_filename,
    save_uploaded_file,
)
from backend.app.utils.file_validator import (
    validate_resume_file,
)

logger = logging.getLogger(__name__)

PARSER_VERSION = "1.0.0"


def upload_resume(
    db: Session,
    user,
    title: str,
    upload_file: UploadFile,
):
    """
    Upload and process a resume.

    Workflow
    --------
    1. Validate file
    2. Store file
    3. Create resume record
    4. Parse resume
    5. Extract structured information
    6. Persist skills
    7. Persist experiences
    8. Update parsing metadata
    """

    validate_resume_file(upload_file)

    filename = upload_file.filename

    if filename is None:
        raise InvalidResumeFileException()

    stored_filename = generate_uuid_filename(
        filename,
    )

    user_directory = create_user_storage_directory(
        user.id,
    )

    destination = user_directory / stored_filename

    save_uploaded_file(
        upload_file,
        destination,
    )

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

    try:

        logger.info(
            "Parsing resume %s",
            resume.id,
        )

        parsed = parse_resume(
            str(destination),
        )

        normalized_text = parsed["normalized_text"]

        resume.parsed_text = normalized_text
        resume.parser_version = PARSER_VERSION
        resume.parsed_at = datetime.utcnow()

        # =====================================================
        # Structured Resume Information
        # =====================================================

        resume_information = extract_profile(
            normalized_text,
        )

        # =====================================================
        # Skills
        # =====================================================

        skills = build_skills(
            normalized_text,
        )

        ResumeSkillRepository(
            db,
        ).save_skills(
            resume_id=resume.id,
            skills=skills,
        )

        # =====================================================
        # Experiences
        # =====================================================

        ResumeExperienceRepository(
            db,
        ).save_many(
            resume_id=resume.id,
            experiences=[
                asdict(exp)
                for exp in resume_information.experiences
            ],
        )

        # =====================================================
        # Profile
        # =====================================================
        #
        # Intentionally skipped.
        #
        # ResumeInformation currently does not expose
        # structured profile fields (full_name, email,
        # phone, linkedin, github, etc.).
        #
        # Profile persistence will be enabled when the
        # Profile Extractor is implemented.
        #
        # =====================================================

        resume = update_resume(
            db=db,
            resume=resume,
        )

        logger.info(
            "Resume %s processed successfully",
            resume.id,
        )

    except Exception:

        logger.exception(
            "Resume processing failed for resume_id=%s",
            resume.id,
        )

    return ApiResponse(
        success=True,
        message="Resume uploaded successfully.",
        data=ResumeResponse.model_validate(
            resume,
        ),
    )