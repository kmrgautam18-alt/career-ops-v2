"""
OAuth Service — Social Login with Google and GitHub.
Uses Authlib to handle OAuth 2.0 flows.
"""

from __future__ import annotations

import logging
import secrets
from typing import Any

from authlib.integrations.starlette_client import OAuth
from starlette.config import Config

from backend.app.core.config import settings
from backend.app.models.user import User
from backend.app.security.password import hash_password

logger = logging.getLogger(__name__)

# ── OAuth Client ────────────────────────────────────────────────────────

starlette_config = Config(environ={
    "GOOGLE_CLIENT_ID": settings.GOOGLE_CLIENT_ID or "",
    "GOOGLE_CLIENT_SECRET": settings.GOOGLE_CLIENT_SECRET or "",
    "GITHUB_CLIENT_ID": settings.GITHUB_CLIENT_ID or "",
    "GITHUB_CLIENT_SECRET": settings.GITHUB_CLIENT_SECRET or "",
})

oauth = OAuth(starlette_config)

oauth.register(
    name="google",
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

oauth.register(
    name="github",
    access_token_url="https://github.com/login/oauth/access_token",
    access_token_params=None,
    authorize_url="https://github.com/login/oauth/authorize",
    authorize_params=None,
    api_base_url="https://api.github.com/",
    client_kwargs={"scope": "user:email"},
)


# ── OAuth Providers ────────────────────────────────────────────────────

OAUTH_PROVIDERS = {
    "google": {
        "authorization_url": "https://accounts.google.com/o/oauth2/auth",
        "token_url": "https://oauth2.googleapis.com/token",
        "userinfo_url": "https://www.googleapis.com/oauth2/v2/userinfo",
        "scopes": ["openid", "email", "profile"],
    },
    "github": {
        "authorization_url": "https://github.com/login/oauth/authorize",
        "token_url": "https://github.com/login/oauth/access_token",
        "userinfo_url": "https://api.github.com/user",
        "scopes": ["user:email"],
    },
}


# ── Functions ──────────────────────────────────────────────────────────


def get_authorization_url(provider: str, redirect_uri: str) -> str:
    """
    Generate the OAuth authorization URL for a provider.

    Args:
        provider: 'google' or 'github'
        redirect_uri: Full callback URL

    Returns:
        Authorization URL to redirect the user to
    """
    provider_config = OAUTH_PROVIDERS.get(provider)
    if not provider_config:
        raise ValueError(f"Unsupported OAuth provider: {provider}")

    state = secrets.token_urlsafe(32)

    params = {
        "client_id": settings.GOOGLE_CLIENT_ID if provider == "google" else settings.GITHUB_CLIENT_ID,
        "redirect_uri": redirect_uri,
        "scope": " ".join(provider_config["scopes"]),
        "state": state,
        "response_type": "code",
        "access_type": "offline",
    }

    url = f"{provider_config['authorization_url']}?{'&'.join(f'{k}={v}' for k, v in params.items())}"
    logger.info("Generated OAuth URL for %s: %s", provider, url[:80] + "...")

    return url


def exchange_code_for_token(provider: str, code: str, redirect_uri: str) -> dict[str, Any] | None:
    """
    Exchange the authorization code for an access token.

    Args:
        provider: 'google' or 'github'
        code: Authorization code from the OAuth callback
        redirect_uri: Must match the original redirect URI

    Returns:
        Token data dict or None on failure
    """
    import requests

    provider_config = OAUTH_PROVIDERS.get(provider)
    if not provider_config:
        return None

    try:
        client_id = settings.GOOGLE_CLIENT_ID if provider == "google" else settings.GITHUB_CLIENT_ID
        client_secret = settings.GOOGLE_CLIENT_SECRET if provider == "google" else settings.GITHUB_CLIENT_SECRET

        response = requests.post(
            provider_config["token_url"],
            data={
                "client_id": client_id,
                "client_secret": client_secret,
                "code": code,
                "redirect_uri": redirect_uri,
                "grant_type": "authorization_code",
            },
            headers={"Accept": "application/json"},
            timeout=10,
        )
        response.raise_for_status()
        return response.json()  # type: ignore[no-any-return]
    except Exception as e:
        logger.error("OAuth token exchange failed for %s: %s", provider, e)
        return None


def fetch_user_info(provider: str, access_token: str) -> dict[str, Any] | None:
    """
    Fetch user information from the OAuth provider using the access token.

    Args:
        provider: 'google' or 'github'
        access_token: OAuth access token

    Returns:
        User info dict with at minimum 'email' and 'name' fields
    """
    import requests

    provider_config = OAUTH_PROVIDERS.get(provider)
    if not provider_config:
        return None

    try:
        response = requests.get(
            provider_config["userinfo_url"],
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()

        # Normalize user info
        if provider == "google":
            return {
                "provider": "google",
                "provider_id": data.get("id"),
                "email": data.get("email", ""),
                "name": data.get("name", ""),
                "avatar_url": data.get("picture"),
                "verified": data.get("verified_email", False),
            }
        elif provider == "github":
            # GitHub might not return email in user info
            email = data.get("email", "")
            if not email:
                try:
                    email_response = requests.get(
                        "https://api.github.com/user/emails",
                        headers={"Authorization": f"Bearer {access_token}"},
                        timeout=10,
                    )
                    email_response.raise_for_status()
                    emails = email_response.json()
                    primary = [e for e in emails if e.get("primary")]
                    email = primary[0]["email"] if primary else (emails[0]["email"] if emails else "")
                except Exception:
                    pass

            return {
                "provider": "github",
                "provider_id": str(data.get("id", "")),
                "email": email,
                "name": data.get("name") or data.get("login", ""),
                "avatar_url": data.get("avatar_url"),
                "verified": True,
            }

        return data
    except Exception as e:
        logger.error("Failed to fetch user info from %s: %s", provider, e)
        return None


def create_or_get_oauth_user(db_session, user_info: dict[str, Any]) -> User:
    """
    Find an existing user by OAuth provider ID or email, or create a new one.

    Args:
        db_session: SQLAlchemy session
        user_info: Dict with provider, provider_id, email, name

    Returns:
        User model instance
    """
    from backend.app.repositories.user_repository_sa import get_user_by_email

    email = user_info.get("email", "")
    name = user_info.get("name", "OAuth User")
    provider = user_info.get("provider", "unknown")

    # Try to find existing user by email
    user = get_user_by_email(db_session, email) if email else None

    if user:
        # Update existing user's OAuth info
        if provider == "google":
            user.google_id = user_info.get("provider_id")
        elif provider == "github":
            user.github_id = user_info.get("provider_id")
        user.is_verified = True
        db_session.commit()
        logger.info("Linked OAuth %s to existing user: %s", provider, email)
        return user

    # Create new user
    random_password = secrets.token_urlsafe(32)
    username = email.split("@")[0] if email else f"user_{secrets.token_hex(4)}"
    # Ensure unique username
    existing = db_session.query(User).filter(User.username == username).first()
    if existing:
        username = f"{username}_{secrets.token_hex(2)}"

    user = User(
        email=email or f"{provider}_{user_info.get('provider_id', 'unknown')}@oauth.local",
        username=username,
        full_name=name,
        hashed_password=hash_password(random_password),
        is_active=True,
        is_verified=True,
    )

    if provider == "google":
        user.google_id = user_info.get("provider_id")
    elif provider == "github":
        user.github_id = user_info.get("provider_id")

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    logger.info("Created new user via %s: %s", provider, user.email)
    return user


def login_with_oauth(
    db_session,
    provider: str,
    code: str,
    redirect_uri: str,
) -> dict[str, Any] | None:
    """
    Complete OAuth login flow: exchange code → fetch user → create/get user → generate JWT.

    Args:
        db_session: SQLAlchemy session
        provider: 'google' or 'github'
        code: Authorization code from callback
        redirect_uri: Original redirect URI

    Returns:
        Dict with access_token, refresh_token, user or None on failure
    """
    from backend.app.security.jwt import create_access_token, create_refresh_token

    # Step 1: Exchange code for token
    token_data = exchange_code_for_token(provider, code, redirect_uri)
    if not token_data:
        logger.error("OAuth token exchange failed for %s", provider)
        return None

    access_token = token_data.get("access_token")
    if not access_token:
        logger.error("No access token in OAuth response for %s", provider)
        return None

    # Step 2: Fetch user info
    user_info = fetch_user_info(provider, access_token)
    if not user_info:
        logger.error("Failed to fetch user info from %s", provider)
        return None

    # Step 3: Create or get user
    user = create_or_get_oauth_user(db_session, user_info)

    # Step 4: Generate JWT tokens
    jwt_access = create_access_token(
        user_id=user.id,
        email=user.email,
        role=user.role,
    )
    jwt_refresh = create_refresh_token(
        user_id=user.id,
    )

    return {
        "access_token": jwt_access,
        "refresh_token": jwt_refresh,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "full_name": user.full_name,
            "role": user.role,
            "is_active": user.is_active,
        },
    }
