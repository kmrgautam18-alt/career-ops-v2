from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.application import Application


def get_all_applications(
    db: Session,
    user_id: int,
):
    """
    Retrieve all applications for a specific user.
    """

    return db.scalars(
        select(Application)
        .where(Application.user_id == user_id)
        .order_by(Application.id)
    ).all()


def get_application_by_id(
    db: Session,
    application_id: int,
):
    """
    Retrieve an application by ID.
    """

    return db.get(Application, application_id)


def get_application_by_user_and_job(
    db: Session,
    user_id: int,
    job_id: int,
):
    """
    Return an existing application for the given user and job.
    """

    return db.scalar(
        select(Application).where(
            Application.user_id == user_id,
            Application.job_id == job_id,
        )
    )


def create_application(
    db: Session,
    user_id: int,
    job_id: int,
    applied_date: date,
    status: str,
    notes: str | None,
):
    """
    Create a new application.
    """

    application = Application(
        user_id=user_id,
        job_id=job_id,
        applied_date=applied_date,
        status=status,
        notes=notes,
    )

    db.add(application)
    db.commit()
    db.refresh(application)

    return application


def update_application(
    db: Session,
    application_id: int,
    applied_date: date,
    status: str,
    notes: str | None,
):
    """
    Update an existing application.
    """

    application = db.get(Application, application_id)

    if application is None:
        return None

    application.applied_date = applied_date
    application.status = status
    application.notes = notes

    db.commit()
    db.refresh(application)

    return application


def delete_application(
    db: Session,
    application_id: int,
):
    """
    Delete an application.
    """

    application = db.get(Application, application_id)

    if application is None:
        return False

    db.delete(application)
    db.commit()

    return True