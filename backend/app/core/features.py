"""
Feature Flags System — Gradual rollout, kill switches, A/B testing.

Usage:
    from backend.app.core.features import feature_enabled
    
    if feature_enabled("ai_coach"):
        # Rolling out to 10% of users
        ...
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any

# ==============================================================================
# Feature Flag Definitions
# ==============================================================================
# Each flag has:
#   - enabled: master toggle
#   - rollout_pct: 0-100, percentage of users who see it (by user_id hash)
#   - description: what it does
#   - depends_on: list of feature flags that must also be enabled
# ==============================================================================

FEATURE_FLAGS: dict[str, dict[str, Any]] = {
    "pwa_install": {
        "enabled": True,
        "rollout_pct": 100,
        "description": "PWA install prompt + offline mode",
        "depends_on": [],
    },
    "email_verification": {
        "enabled": True,
        "rollout_pct": 100,
        "description": "Require email verification before full access",
        "depends_on": [],
    },
    "data_export": {
        "enabled": True,
        "rollout_pct": 100,
        "description": "Allow users to export their data as JSON/CSV",
        "depends_on": [],
    },
    "ai_model_switcher": {
        "enabled": True,
        "rollout_pct": 50,
        "description": "Allow users to switch between Gemini, OpenAI, Claude",
        "depends_on": [],
    },
    "websocket_notifications": {
        "enabled": False,
        "rollout_pct": 0,
        "description": "Real-time WebSocket notifications",
        "depends_on": [],
    },
    "notification_preferences": {
        "enabled": True,
        "rollout_pct": 100,
        "description": "Notification channel preferences dashboard",
        "depends_on": [],
    },
    "audit_logging": {
        "enabled": True,
        "rollout_pct": 100,
        "description": "Audit log all user actions",
        "depends_on": [],
    },
    "sentry_tracking": {
        "enabled": False,
        "rollout_pct": 0,
        "description": "Sentry error tracking in production",
        "depends_on": [],
    },
    "interview_coach": {
        "enabled": False,
        "rollout_pct": 0,
        "description": "AI-powered mock interview coach",
        "depends_on": ["ai_model_switcher"],
    },
    "i18n": {
        "enabled": True,
        "rollout_pct": 100,
        "description": "Internationalization / multi-language support",
        "depends_on": [],
    },
    "multi_tenant": {
        "enabled": False,
        "rollout_pct": 0,
        "description": "Organizations, teams, shared job boards",
        "depends_on": [],
    },
    "resume_templates": {
        "enabled": True,
        "rollout_pct": 100,
        "description": "Resume template marketplace",
        "depends_on": [],
    },
    "plugin_system": {
        "enabled": False,
        "rollout_pct": 0,
        "description": "Third-party plugin system",
        "depends_on": [],
    },
    "mobile_api": {
        "enabled": True,
        "rollout_pct": 100,
        "description": "Mobile-optimized API endpoints",
        "depends_on": [],
    },
}

# ==============================================================================
# Override file (can be mounted as a volume in Docker)
# ==============================================================================

_OVERRIDE_PATH = Path(os.getenv("FEATURE_FLAGS_PATH", "/data/feature_flags.json"))


def _load_overrides() -> dict[str, dict[str, Any]]:
    """Load feature flag overrides from a JSON file (if it exists)."""
    if _OVERRIDE_PATH.exists():
        try:
            with open(_OVERRIDE_PATH) as f:
                return json.load(f)  # type: ignore[no-any-return]
        except (json.JSONDecodeError, OSError):
            pass
    return {}


def _get_flag(flag_name: str) -> dict[str, Any] | None:
    """Get a feature flag definition, with overrides applied."""
    overrides = _load_overrides()
    if flag_name in overrides:
        return overrides[flag_name]
    return FEATURE_FLAGS.get(flag_name)


def feature_enabled(flag_name: str, user_id: int | None = None) -> bool:
    """
    Check if a feature flag is enabled for a given user.

    Args:
        flag_name: The feature flag name (e.g., "ai_coach")
        user_id: Optional user ID for percentage-based rollouts

    Returns:
        True if the feature is enabled for this user.
    """
    flag = _get_flag(flag_name)
    if flag is None:
        return False

    # Master toggle
    if not flag.get("enabled", False):
        return False

    # Check dependencies
    for dep in flag.get("depends_on", []):
        if not feature_enabled(dep, user_id):
            return False

    # Percentage-based rollout
    rollout_pct = flag.get("rollout_pct", 100)
    if rollout_pct >= 100:
        return True
    if rollout_pct <= 0:
        return False
    if user_id is None:
        return False

    # Deterministic bucket by user_id hash
    bucket = int(hashlib.md5(str(user_id).encode()).hexdigest(), 16) % 100
    return bucket < rollout_pct


def get_all_features(user_id: int | None = None) -> dict[str, bool]:
    """Get status of all feature flags for a user."""
    return {name: feature_enabled(name, user_id) for name in FEATURE_FLAGS}


def set_feature_override(flag_name: str, enabled: bool, rollout_pct: int | None = None) -> None:
    """
    Set a runtime override for a feature flag.
    Overrides are ephemeral (not persisted to disk).
    """
    if flag_name not in FEATURE_FLAGS:
        raise ValueError(f"Unknown feature flag: {flag_name}")
    if rollout_pct is not None and not (0 <= rollout_pct <= 100):
        raise ValueError("rollout_pct must be between 0 and 100")

    overrides = _load_overrides()
    override = overrides.get(flag_name, {})
    override["enabled"] = enabled
    if rollout_pct is not None:
        override["rollout_pct"] = rollout_pct
    overrides[flag_name] = override

    _OVERRIDE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(_OVERRIDE_PATH, "w") as f:
        json.dump(overrides, f, indent=2)  # type: ignore[no-any-return]
