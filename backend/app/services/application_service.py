from sqlalchemy.orm import Session

from backend.app.exceptions.custom_exceptions import (
    ApplicationNotFoundException,
)
from backend.app.repositories.application_repository_sa import (
    create_application,
    delete_application,
    get_application_by_id_and_user,
    get_application_by_user_and_job,
    get_applications_by_user,
    update_application,
)
from backend.app.schemas.application_schema import (
    ApplicationCreate,
    ApplicationResponse,
    ApplicationUpdate,
)
from backend.app.schemas.common_schema import ApiResponse


def list_applications(
    db: Session,
    user_id: int,
):
    """
    Retrieve all applications for the authenticated user.
    """

    applications = get_applications_by_user(
        db=db,
        user_id=user_id,
    )

    return ApiResponse(
        success=True,
        message="Applications retrieved successfully.",
        data=[
            ApplicationResponse.model_validate(application)
            for application in applications
        ],
    )


def get_application(
    db: Session,
    user_id: int,
    application_id: int,
):
    """
    Retrieve a single application owned by the authenticated user.
    """

    application = get_application_by_id_and_user(
        db=db,
        application_id=application_id,
        user_id=user_id,
    )

    if application is None:
        raise ApplicationNotFoundException(
            application_id
        )

    return ApiResponse(
        success=True,
        message="Application retrieved successfully.",
        data=ApplicationResponse.model_validate(
            application
        ),
    )


def create_new_application(
    db: Session,
    user_id: int,
    application: ApplicationCreate,
):
    """
    Create a new application.
    """

    existing = get_application_by_user_and_job(
        db=db,
        user_id=user_id,
        job_id=application.job_id,
    )

    if existing is not None:
        return ApiResponse(
            success=False,
            message="You have already applied for this job.",
            data=None,
        )

    created_application = create_application(
        db=db,
        user_id=user_id,
        job_id=application.job_id,
        applied_date=application.applied_date,
        status=application.status,
        notes=application.notes,
    )

    return ApiResponse(
        success=True,
        message="Application created successfully.",
        data=ApplicationResponse.model_validate(
            created_application,
        ),
    )


def update_existing_application(
    db: Session,
    user_id: int,
    application_id: int,
    application: ApplicationUpdate,
):
    """
    Update an existing application.
    """

    existing = get_application_by_id_and_user(
        db=db,
        application_id=application_id,
        user_id=user_id,
    )

    if existing is None:
        raise ApplicationNotFoundException(
            application_id
        )

    if application.applied_date is not None:
        existing.applied_date = (
            application.applied_date
        )

    if application.status is not None:
        existing.status = application.status

    if application.notes is not None:
        existing.notes = application.notes

    updated = update_application(
        db=db,
        application=existing,
    )

    return ApiResponse(
        success=True,
        message="Application updated successfully.",
        data=ApplicationResponse.model_validate(
            updated
        ),
    )


def remove_application(
    db: Session,
    user_id: int,
    application_id: int,
):
    """
    Delete an application owned by the authenticated user.
    """

    application = get_application_by_id_and_user(
        db=db,
        application_id=application_id,
        user_id=user_id,
    )

    if application is None:
        raise ApplicationNotFoundException(
            application_id
        )

    delete_application(
        db=db,
        application=application,
    )

    return ApiResponse(
        success=True,
        message="Application deleted successfully.",
        data={
            "application_id": application_id,
        },
    )