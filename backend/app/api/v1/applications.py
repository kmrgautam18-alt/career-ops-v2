from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.database.dependencies import get_db
from backend.app.schemas.application_schema import (
    ApplicationCreate,
    ApplicationUpdate,
)
from backend.app.security.dependencies import (
    get_current_active_user,
)
from backend.app.services.application_service import (
    create_new_application,
    get_application,
    list_applications,
    remove_application,
    update_existing_application,
)

router = APIRouter(
    prefix="/applications",
    tags=["Applications"],
)


@router.get("")
def get_my_applications(
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Return all applications belonging to the authenticated user.
    """

    return list_applications(
        db=db,
        user_id=current_user.id,
    )


@router.get("/{application_id}")
def get_application_endpoint(
    application_id: int,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Return a single application belonging to the authenticated user.
    """

    return get_application(
        db=db,
        user_id=current_user.id,
        application_id=application_id,
    )


@router.post("")
def create_application_endpoint(
    application: ApplicationCreate,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Create a new job application.
    """

    return create_new_application(
        db=db,
        user_id=current_user.id,
        application=application,
    )


@router.patch("/{application_id}")
def update_application_endpoint(
    application_id: int,
    application: ApplicationUpdate,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Update an existing application.
    """

    return update_existing_application(
        db=db,
        user_id=current_user.id,
        application_id=application_id,
        application=application,
    )


@router.delete("/{application_id}")
def delete_application_endpoint(
    application_id: int,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Delete an application.
    """

    return remove_application(
        db=db,
        user_id=current_user.id,
        application_id=application_id,
    )
