"""
Email Verification API endpoints.
"""

import logging

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from backend.app.database.dependencies import get_db
from backend.app.repositories.user_repository_sa import get_user_by_id, update_user
from backend.app.security.dependencies import get_current_active_user
from backend.app.services.email_verification import (
    send_password_reset_email,
    send_verification_email,
    verify_email_token,
    verify_password_reset_token,
)
from backend.app.security.password import hash_password

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/auth",
    tags=["Email Verification"],
)


@router.post("/send-verification")
def request_verification(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """Send a verification email to the current user."""
    if current_user.is_verified:
        return {"success": True, "message": "Email already verified."}

    success = send_verification_email(db, current_user)
    if success:
        return {"success": True, "message": "Verification email sent."}
    raise HTTPException(status_code=500, detail="Failed to send verification email.")


@router.get("/verify-email")
def verify_email(
    user_id: int = Query(...),
    token: str = Query(...),
    db: Session = Depends(get_db),
):
    """Verify a user's email address using a token."""
    valid = verify_email_token(user_id, token)
    if not valid:
        raise HTTPException(status_code=400, detail="Invalid or expired verification token.")

    user = get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found.")

    user.is_verified = True
    update_user(db, user)

    return {"success": True, "message": "Email verified successfully."}


@router.post("/forgot-password")
def forgot_password(
    email: str = Query(...),
    db: Session = Depends(get_db),
):
    """Send a password reset email."""
    from backend.app.repositories.user_repository_sa import get_user_by_email

    user = get_user_by_email(db, email)
    if user is None:
        # Don't reveal if email exists
        return {"success": True, "message": "If the email exists, a reset link has been sent."}

    success = send_password_reset_email(db, user)
    if success:
        return {"success": True, "message": "If the email exists, a reset link has been sent."}
    raise HTTPException(status_code=500, detail="Failed to send reset email.")


@router.post("/reset-password")
def reset_password(
    user_id: int = Query(...),
    token: str = Query(...),
    new_password: str = Query(..., min_length=8),
    db: Session = Depends(get_db),
):
    """Reset a user's password using a valid reset token."""
    valid = verify_password_reset_token(user_id, token)
    if not valid:
        raise HTTPException(status_code=400, detail="Invalid or expired reset token.")

    user = get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found.")

    user.hashed_password = hash_password(new_password)
    update_user(db, user)

    return {"success": True, "message": "Password reset successfully."}
