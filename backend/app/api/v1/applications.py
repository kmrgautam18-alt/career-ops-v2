from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.database.dependencies import get_db
from backend.app.schemas.application_schema import (
    ApplicationCreate,
    ApplicationUpdate,
)
from backend.app.security.dependencies import get_current_active_user
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


@router.get("/health")
def health():
    return {"status": "ok"}


@router.get("")
def get_all_applications(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    return list_applications(
        db=db,
        user_id=current_user.id,
    )


@router.post("")
def create_application(
    application: ApplicationCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    return create_new_application(
        db=db,
        user_id=current_user.id,
        application=application,
    )


@router.get("/{application_id}")
def get_single_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    return get_application(
        db=db,
        application_id=application_id,
    )


@router.put("/{application_id}")
def update_application(
    application_id: int,
    application: ApplicationUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    return update_existing_application(
        db=db,
        application_id=application_id,
        application=application,
    )


@router.delete("/{application_id}")
def delete_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    return remove_application(
        db=db,
        application_id=application_id,
    )