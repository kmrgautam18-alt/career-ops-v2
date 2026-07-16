"""
OAuth API Router — Social Login Endpoints.
Provides endpoints for Google and GitHub authentication.
"""

from __future__ import annotations

import logging

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session

from backend.app.database.dependencies import get_db
from backend.app.services.oauth_service import (
    get_authorization_url,
    login_with_oauth,
)

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/auth/oauth",
    tags=["OAuth"],
)


@router.get("/{provider}/login")
def oauth_login(
    provider: str,
    request: Request,
    redirect: str = Query("/dashboard", description="Where to redirect after login"),
):
    """
    Initiate OAuth login with the specified provider.
    Redirects the user to the provider's authorization page.

    Args:
        provider: 'google' or 'github'
        redirect: Frontend URL to redirect to after successful login
    """
    if provider not in ("google", "github"):
        raise HTTPException(status_code=400, detail=f"Unsupported provider: {provider}")

    # Build callback URL
    callback_url = str(request.base_url).rstrip("/") + f"/api/v1/auth/oauth/{provider}/callback"
    # Store redirect in state (simplified — would use session in production)
    auth_url = get_authorization_url(provider, callback_url)

    return {
        "success": True,
        "message": f"Redirecting to {provider} for authorization",
        "data": {
            "authorization_url": auth_url,
            "provider": provider,
            "callback_url": callback_url,
            "redirect_after": redirect,
        },
    }


@router.get("/{provider}/callback")
def oauth_callback(
    provider: str,
    code: str = Query(..., description="Authorization code from provider"),
    state: str = Query("", description="OAuth state parameter"),
    request: Request = None,
    db: Session = Depends(get_db),
):
    """
    OAuth callback endpoint — called by the provider after user authorization.
    Exchanges the auth code for tokens and logs the user in.

    Args:
        provider: 'google' or 'github'
        code: Authorization code from the provider
        state: State parameter for CSRF protection
    """
    if provider not in ("google", "github"):
        raise HTTPException(status_code=400, detail=f"Unsupported provider: {provider}")

    callback_url = str(request.base_url).rstrip("/") + f"/api/v1/auth/oauth/{provider}/callback"

    result = login_with_oauth(
        db_session=db,
        provider=provider,
        code=code,
        redirect_uri=callback_url,
    )

    if not result:
        raise HTTPException(
            status_code=401,
            detail=f"OAuth authentication with {provider} failed. Please try again.",
        )

    return {
        "success": True,
        "message": f"Successfully authenticated with {provider}",
        "data": result,
    }
