"""
Email Verification Service.
Generates verification tokens and sends verification emails.
"""

from __future__ import annotations

import logging
import secrets
from datetime import datetime, timedelta
from typing import Any

from sqlalchemy.orm import Session

from backend.app.core.config import settings
from backend.app.models.user import User
from backend.app.services.email_service import send_html_email

logger = logging.getLogger(__name__)

# In-memory token store (use Redis in production)
_verification_tokens: dict[int, dict[str, Any]] = {}
_PASSWORD_RESET_TOKENS: dict[int, dict[str, Any]] = {}

TOKEN_EXPIRY_HOURS = 48
RESET_EXPIRY_HOURS = 1


def _generate_token() -> str:
    """Generate a cryptographically secure token."""
    return secrets.token_urlsafe(48)


def send_verification_email(db: Session, user: User) -> bool:
    """Generate a verification token and send the verification email."""
    token = _generate_token()
    expiry = datetime.utcnow() + timedelta(hours=TOKEN_EXPIRY_HOURS)

    _verification_tokens[user.id] = {
        "token": token,
        "expires_at": expiry,
    }

    app_url = getattr(settings, 'APP_URL', None) or 'http://localhost:5173'
    verify_url = f"{app_url}/verify-email?token={token}&user_id={user.id}"

    subject = "Verify your Career-Ops account"
    html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background: #0d0d1a; color: #e8eaf0; padding: 40px;">
        <div style="max-width: 480px; margin: 0 auto; background: #14142a; border-radius: 16px; padding: 32px; border: 1px solid #2a2a50;">
            <h1 style="color: #6366f1; margin: 0 0 16px;">Welcome to Career-Ops 🚀</h1>
            <p style="color: #8892b0; line-height: 1.6;">
                Hi <strong style="color: #e8eaf0;">{user.full_name}</strong>,
            </p>
            <p style="color: #8892b0; line-height: 1.6;">
                Please verify your email address to activate your account and start using all features.
            </p>
            <div style="text-align: center; margin: 28px 0;">
                <a href="{verify_url}" style="display: inline-block; padding: 14px 32px; background: linear-gradient(135deg, #6366f1, #22d3ee); color: white; text-decoration: none; border-radius: 12px; font-weight: 600; font-size: 15px;">
                    Verify Email Address
                </a>
            </div>
            <p style="color: #5a6080; font-size: 12px; margin-top: 24px;">
                This link expires in {TOKEN_EXPIRY_HOURS} hours. If you didn't create an account, ignore this email.
            </p>
        </div>
    </body>
    </html>
    """

    return send_html_email(
        to_email=user.email,
        to_name=user.full_name,
        subject=subject,
        html_content=html,
    )


def verify_email_token(user_id: int, token: str) -> bool:
    """Verify an email verification token."""
    record = _verification_tokens.get(user_id)
    if record is None:
        logger.warning(f"No verification token found for user {user_id}")
        return False

    if record["token"] != token:
        logger.warning(f"Invalid verification token for user {user_id}")
        return False

    if datetime.utcnow() > record["expires_at"]:
        logger.warning(f"Expired verification token for user {user_id}")
        _verification_tokens.pop(user_id, None)
        return False

    _verification_tokens.pop(user_id, None)
    return True


def send_password_reset_email(db: Session, user: User) -> bool:
    """Send a password reset email."""
    token = _generate_token()
    expiry = datetime.utcnow() + timedelta(hours=RESET_EXPIRY_HOURS)

    _PASSWORD_RESET_TOKENS[user.id] = {
        "token": token,
        "expires_at": expiry,
    }

    app_url = getattr(settings, 'APP_URL', None) or 'http://localhost:5173'
    reset_url = f"{app_url}/reset-password?token={token}&user_id={user.id}"

    subject = "Reset your Career-Ops password"
    html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background: #0d0d1a; color: #e8eaf0; padding: 40px;">
        <div style="max-width: 480px; margin: 0 auto; background: #14142a; border-radius: 16px; padding: 32px; border: 1px solid #2a2a50;">
            <h1 style="color: #6366f1; margin: 0 0 16px;">Password Reset</h1>
            <p style="color: #8892b0; line-height: 1.6;">
                Click the link below to reset your password. This link expires in 1 hour.
            </p>
            <div style="text-align: center; margin: 28px 0;">
                <a href="{reset_url}" style="display: inline-block; padding: 14px 32px; background: linear-gradient(135deg, #6366f1, #22d3ee); color: white; text-decoration: none; border-radius: 12px; font-weight: 600; font-size: 15px;">
                    Reset Password
                </a>
            </div>
        </div>
    </body>
    </html>
    """

    return send_html_email(
        to_email=user.email,
        to_name=user.full_name,
        subject=subject,
        html_content=html,
    )


def verify_password_reset_token(user_id: int, token: str) -> bool:
    """Verify a password reset token."""
    record = _PASSWORD_RESET_TOKENS.get(user_id)
    if record is None:
        return False
    if record["token"] != token:
        return False
    if datetime.utcnow() > record["expires_at"]:
        _PASSWORD_RESET_TOKENS.pop(user_id, None)
        return False
    _PASSWORD_RESET_TOKENS.pop(user_id, None)
    return True
