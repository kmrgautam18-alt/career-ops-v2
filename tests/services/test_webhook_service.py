"""
Unit tests for the n8n webhook integration service.

Tests cover:
- _send_webhook with n8n disabled/enabled
- All three notify_* functions
- Payload structure
- Error handling (connection failures)
"""

from unittest.mock import patch

import pytest
import requests

from backend.app.core.config import settings
from backend.app.services.webhook_service import (
    _send_webhook,
    notify_application_created,
    notify_application_deleted,
    notify_application_updated,
)

# ── Fixtures ────────────────────────────────────────────────────────────


@pytest.fixture(autouse=True)
def reset_n8n_settings():
    """Reset n8n settings before and after each test."""
    original_enabled = settings.N8N_ENABLED
    original_url = settings.N8N_WEBHOOK_BASE_URL
    yield
    settings.N8N_ENABLED = original_enabled
    settings.N8N_WEBHOOK_BASE_URL = original_url


# ── _send_webhook tests ─────────────────────────────────────────────────


class TestSendWebhook:
    def test_disabled_returns_false(self):
        """When N8N_ENABLED is False, _send_webhook should return False without calling HTTP."""
        settings.N8N_ENABLED = False
        settings.N8N_WEBHOOK_BASE_URL = "http://n8n:5678"

        result = _send_webhook("test-event", {"key": "value"})

        assert result is False

    @patch("backend.app.services.webhook_service.requests.post")
    def test_enabled_successful_send(self, mock_post):
        """When N8N_ENABLED is True and HTTP succeeds, _send_webhook should return True."""
        settings.N8N_ENABLED = True
        settings.N8N_WEBHOOK_BASE_URL = "http://n8n:5678"

        mock_response = mock_post.return_value
        mock_response.raise_for_status.return_value = None
        mock_response.status_code = 200

        result = _send_webhook("careerops-test", {"msg": "hello"})

        assert result is True
        mock_post.assert_called_once_with(
            "http://n8n:5678/webhook/careerops-test",
            json={"msg": "hello"},
            timeout=5,
        )

    @patch("backend.app.services.webhook_service.requests.post")
    def test_enabled_http_error(self, mock_post):
        """When n8n returns a non-2xx status, _send_webhook should return False."""
        settings.N8N_ENABLED = True
        settings.N8N_WEBHOOK_BASE_URL = "http://n8n:5678"

        mock_response = mock_post.return_value
        mock_response.raise_for_status.side_effect = (
            requests.HTTPError("404 Client Error")
        )

        result = _send_webhook("test-event", {"key": "value"})

        assert result is False

    @patch("backend.app.services.webhook_service.requests.post")
    def test_enabled_connection_error(self, mock_post):
        """When n8n is unreachable, _send_webhook should return False."""
        settings.N8N_ENABLED = True
        settings.N8N_WEBHOOK_BASE_URL = "http://n8n:5678"

        mock_post.side_effect = requests.ConnectionError("Connection refused")

        result = _send_webhook("test-event", {"key": "value"})

        assert result is False

    @patch("backend.app.services.webhook_service.requests.post")
    def test_enabled_timeout_error(self, mock_post):
        """When n8n times out, _send_webhook should return False."""
        settings.N8N_ENABLED = True
        settings.N8N_WEBHOOK_BASE_URL = "http://n8n:5678"

        mock_post.side_effect = requests.Timeout("Request timed out")

        result = _send_webhook("test-event", {"key": "value"})

        assert result is False

    @patch("backend.app.services.webhook_service.requests.post")
    def test_url_uses_correct_webhook_path(self, mock_post):
        """Verify the URL is constructed as: base_url/webhook/{event}."""
        settings.N8N_ENABLED = True
        settings.N8N_WEBHOOK_BASE_URL = "http://n8n:5678"

        mock_response = mock_post.return_value
        mock_response.raise_for_status.return_value = None
        mock_response.status_code = 200

        _send_webhook("my-event", {})

        called_url = mock_post.call_args[0][0]
        assert called_url == "http://n8n:5678/webhook/my-event"

    @patch("backend.app.services.webhook_service.requests.post")
    def test_url_strips_trailing_slash(self, mock_post):
        """If BASE_URL has a trailing slash, it should be stripped."""
        settings.N8N_ENABLED = True
        settings.N8N_WEBHOOK_BASE_URL = "http://n8n:5678/"

        mock_response = mock_post.return_value
        mock_response.raise_for_status.return_value = None
        mock_response.status_code = 200

        _send_webhook("test", {})

        called_url = mock_post.call_args[0][0]
        assert called_url == "http://n8n:5678/webhook/test"
        # Ensure there's no double slash
        assert "//webhook" not in called_url.replace("://", "||")


# ── notify_application_created tests ────────────────────────────────────


class TestNotifyApplicationCreated:
    @patch("backend.app.services.webhook_service._send_webhook")
    def test_sends_correct_event(self, mock_send):
        """Should send the 'careerops-application-created' event."""
        settings.N8N_ENABLED = True

        notify_application_created(
            user_id=1,
            user_email="user@test.com",
            application_id=10,
            job_id=5,
            company="Google",
            job_title="Engineer",
            status="Applied",
            applied_date="2026-07-15",
        )

        mock_send.assert_called_once()
        event = mock_send.call_args[0][0]
        assert event == "careerops-application-created"

    @patch("backend.app.services.webhook_service._send_webhook")
    def test_payload_structure(self, mock_send):
        """Verify all expected fields are in the payload."""
        settings.N8N_ENABLED = True

        notify_application_created(
            user_id=42,
            user_email="alice@example.com",
            application_id=100,
            job_id=7,
            company="Microsoft",
            job_title="Senior DevOps",
            status="Applied",
            applied_date="2026-07-20",
        )

        payload = mock_send.call_args[0][1]
        assert payload["event"] == "application.created"
        assert payload["user_id"] == 42
        assert payload["user_email"] == "alice@example.com"
        assert payload["application_id"] == 100
        assert payload["job_id"] == 7
        assert payload["company"] == "Microsoft"
        assert payload["job_title"] == "Senior DevOps"
        assert payload["status"] == "Applied"
        assert payload["applied_date"] == "2026-07-20"

    @patch("backend.app.services.webhook_service._send_webhook")
    def test_none_company_falls_back(self, mock_send):
        """If company is None, should send 'Unknown'."""
        settings.N8N_ENABLED = True

        notify_application_created(
            user_id=1,
            user_email="u@t.com",
            application_id=1,
            job_id=1,
            company=None,
            job_title=None,
            status="Applied",
            applied_date="2026-07-15",
        )

        payload = mock_send.call_args[0][1]
        assert payload["company"] == "Unknown"
        assert payload["job_title"] == "Unknown"


# ── notify_application_updated tests ────────────────────────────────────


class TestNotifyApplicationUpdated:
    @patch("backend.app.services.webhook_service._send_webhook")
    def test_sends_correct_event(self, mock_send):
        """Should send the 'careerops-application-status' event."""
        settings.N8N_ENABLED = True

        notify_application_updated(
            user_id=1,
            user_email="u@t.com",
            application_id=10,
            job_id=5,
            company="Google",
            job_title="Engineer",
            previous_status="Applied",
            new_status="Interviewing",
            applied_date="2026-07-15",
        )

        event = mock_send.call_args[0][0]
        assert event == "careerops-application-status"

    @patch("backend.app.services.webhook_service._send_webhook")
    def test_payload_includes_previous_and_new_status(self, mock_send):
        """Verify status transition fields are in the payload."""
        settings.N8N_ENABLED = True

        notify_application_updated(
            user_id=1,
            user_email="u@t.com",
            application_id=10,
            job_id=5,
            company="Google",
            job_title="Engineer",
            previous_status="Applied",
            new_status="Offer",
            applied_date="2026-07-15",
        )

        payload = mock_send.call_args[0][1]
        assert payload["event"] == "application.updated"
        assert payload["previous_status"] == "Applied"
        assert payload["status"] == "Offer"


# ── notify_application_deleted tests ────────────────────────────────────


class TestNotifyApplicationDeleted:
    @patch("backend.app.services.webhook_service._send_webhook")
    def test_sends_correct_event(self, mock_send):
        """Should send the 'careerops-application-deleted' event."""
        settings.N8N_ENABLED = True

        notify_application_deleted(
            user_id=1,
            user_email="u@t.com",
            application_id=10,
            job_id=5,
            company="Google",
            job_title="Engineer",
            previous_status="Rejected",
        )

        event = mock_send.call_args[0][0]
        assert event == "careerops-application-deleted"

    @patch("backend.app.services.webhook_service._send_webhook")
    def test_payload_does_not_include_applied_date(self, mock_send):
        """Delete notification should not include applied_date."""
        settings.N8N_ENABLED = True

        notify_application_deleted(
            user_id=1,
            user_email="u@t.com",
            application_id=10,
            job_id=5,
            company="Google",
            job_title="Engineer",
            previous_status="Rejected",
        )

        payload = mock_send.call_args[0][1]
        assert "applied_date" not in payload
        assert payload["event"] == "application.deleted"


# ── E2E Integration Test (simulates the full call chain) ────────────────


@patch("backend.app.services.webhook_service.requests.post")
class TestFullWebhookFlow:
    """Test the full flow from notify → _send_webhook → HTTP POST."""

    def test_create_flow(self, mock_post):
        """Full flow: notify_application_created → HTTP POST with correct data."""
        settings.N8N_ENABLED = True
        mock_response = mock_post.return_value
        mock_response.raise_for_status.return_value = None
        mock_response.status_code = 200

        notify_application_created(
            user_id=1,
            user_email="test@example.com",
            application_id=99,
            job_id=3,
            company="Acme Corp",
            job_title="Developer",
            status="Applied",
            applied_date="2026-07-16",
        )

        mock_post.assert_called_once()
        url, kwargs = mock_post.call_args[0][0], mock_post.call_args.kwargs
        assert "webhook/careerops-application-created" in url
        assert kwargs["json"]["user_email"] == "test@example.com"
        assert kwargs["timeout"] == 5

    def test_update_flow(self, mock_post):
        """Full flow: notify_application_updated → HTTP POST with status transition."""
        settings.N8N_ENABLED = True
        mock_response = mock_post.return_value
        mock_response.raise_for_status.return_value = None
        mock_response.status_code = 200

        notify_application_updated(
            user_id=1,
            user_email="test@example.com",
            application_id=99,
            job_id=3,
            company="Acme Corp",
            job_title="Developer",
            previous_status="Applied",
            new_status="Interviewing",
            applied_date="2026-07-16",
        )

        mock_post.assert_called_once()
        url = mock_post.call_args[0][0]
        json_data = mock_post.call_args.kwargs["json"]
        assert "webhook/careerops-application-status" in url
        assert json_data["previous_status"] == "Applied"
        assert json_data["status"] == "Interviewing"

    def test_delete_flow(self, mock_post):
        """Full flow: notify_application_deleted → HTTP POST with status."""
        settings.N8N_ENABLED = True
        mock_response = mock_post.return_value
        mock_response.raise_for_status.return_value = None
        mock_response.status_code = 200

        notify_application_deleted(
            user_id=1,
            user_email="test@example.com",
            application_id=99,
            job_id=3,
            company="Acme Corp",
            job_title="Developer",
            previous_status="Rejected",
        )

        mock_post.assert_called_once()
        url = mock_post.call_args[0][0]
        json_data = mock_post.call_args.kwargs["json"]
        assert "webhook/careerops-application-deleted" in url
        assert json_data["event"] == "application.deleted"
