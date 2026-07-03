from sqlalchemy.orm import Session

from backend.app.exceptions.custom_exceptions import (
    JobNotFoundException,
)
from backend.app.repositories.application_repository_sa import (
    create_application,
    delete_application,
    get_all_applications,
    get_application_by_id,
    get_application_by_user_and_job,
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

    applications = get_all_applications(
        db=db,
        user_id=user_id,
    )

    application_list = [
        ApplicationResponse.model_validate(application)
        for application in applications
    ]

    return ApiResponse(
        success=True,
        message="Applications retrieved successfully.",
        data={
            "count": len(application_list),
            "applications": application_list,
        },
    )


def get_application(
    db: Session,
    application_id: int,
):
    """
    Retrieve a single application.
    """

    application = get_application_by_id(
        db=db,
        application_id=application_id,
    )

    if application is None:
        raise JobNotFoundException(application_id)

    return ApiResponse(
        success=True,
        message="Application retrieved successfully.",
        data=ApplicationResponse.model_validate(application),
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

    if existing:
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
        data=ApplicationResponse.model_validate(created_application),
    )


def update_existing_application(
    db: Session,
    application_id: int,
    application: ApplicationUpdate,
):
    """
    Update an existing application.
    """

    existing = get_application_by_id(
        db=db,
        application_id=application_id,
    )

    if existing is None:
        raise JobNotFoundException(application_id)

    updated = update_application(
        db=db,
        application_id=application_id,
        applied_date=application.applied_date
        if application.applied_date is not None
        else existing.applied_date,
        status=application.status
        if application.status is not None
        else existing.status,
        notes=application.notes
        if application.notes is not None
        else existing.notes,
    )

    return ApiResponse(
        success=True,
        message="Application updated successfully.",
        data=ApplicationResponse.model_validate(updated),
    )


def remove_application(
    db: Session,
    application_id: int,
):
    """
    Delete an application.
    """

    deleted = delete_application(
        db=db,
        application_id=application_id,
    )

    if not deleted:
        raise JobNotFoundException(application_id)

    return ApiResponse(
        success=True,
        message="Application deleted successfully.",
        data={
            "application_id": application_id,
        },
    )