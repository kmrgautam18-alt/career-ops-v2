"""
Email Service for Auto Job Application Engine.
Sends tailored application emails via SMTP with resume attachment.
"""

import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from backend.app.core.config import settings


def send_html_email(
    to_email: str,
    to_name: str,
    subject: str,
    html_content: str,
) -> bool:
    """
    Send an HTML email.

    Args:
        to_email: Recipient email address
        to_name: Recipient name
        subject: Email subject line
        html_content: HTML body content

    Returns:
        True if sent successfully.
    """
    if not settings.SMTP_ENABLED:
        logger.info("SMTP disabled. Would send to: %s - Subject: %s", to_email, subject)
        return True

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = settings.SMTP_FROM_EMAIL
        msg["To"] = to_email

        # Plain text fallback
        import re
        text_content = re.sub(r"<[^>]+>", "", html_content).strip()
        msg.attach(MIMEText(text_content, "plain"))
        msg.attach(MIMEText(html_content, "html"))

        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=30) as server:
            if settings.SMTP_TLS:
                server.starttls()
            if settings.SMTP_USER:
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(msg)

        logger.info("HTML email sent to %s: %s", to_email, subject)
        return True

    except Exception as e:
        logger.error("HTML email error: %s", e)
        return False

logger = logging.getLogger(__name__)


def send_application_email(
    to_email: str,
    to_name: str,
    job_title: str,
    company: str,
    applicant_name: str,
    resume_text: str,
    cover_letter_text: str | None = None,
) -> bool:
    """
    Send a tailored job application email to HR with the resume inline.

    Args:
        to_email: HR/recruiter email address
        to_name: HR/recruiter name (or "Hiring Team")
        job_title: The job title being applied for
        company: Company name
        applicant_name: The applicant's full name
        resume_text: AI-tailored resume text to include in email body
        cover_letter_text: Optional cover letter text

    Returns:
        True if sent successfully, False otherwise.
    """
    if not settings.SMTP_ENABLED:
        logger.info("SMTP disabled. Would send to: %s for %s at %s", to_email, job_title, company)
        return True  # Pretend success in dev mode

    try:
        msg = MIMEMultipart("mixed")
        msg["Subject"] = f"Application for {job_title} position — {applicant_name}"
        msg["From"] = settings.SMTP_FROM_EMAIL
        msg["To"] = to_email
        msg["Reply-To"] = settings.SMTP_FROM_EMAIL

        # ── Build email body ──────────────────────────────────────────
        body_parts = []

        if cover_letter_text:
            body_parts.append(cover_letter_text)
            body_parts.append("")
            body_parts.append("---")
            body_parts.append("")

        body_parts.append(f"Dear {to_name},")
        body_parts.append("")
        body_parts.append(
            f"I am writing to express my strong interest in the {job_title} position at {company}. "
            f"Below is my tailored resume highlighting my relevant experience and skills."
        )
        body_parts.append("")
        body_parts.append("─" * 40)
        body_parts.append(f"TAILORED RESUME — {applicant_name}")
        body_parts.append("─" * 40)
        body_parts.append("")
        body_parts.append(resume_text)
        body_parts.append("")
        body_parts.append("─" * 40)
        body_parts.append("")
        body_parts.append(
            "I would welcome the opportunity to discuss how my experience aligns with "
            f"the needs of {company}. I am available for an interview at your convenience."
        )
        body_parts.append("")
        body_parts.append("Best regards,")
        body_parts.append(applicant_name)
        body_parts.append(settings.SMTP_FROM_EMAIL)

        body_text = "\n".join(body_parts)

        # Plain text body
        msg.attach(MIMEText(body_text, "plain"))

        # HTML body for richer formatting
        html_body = body_text.replace("\n", "<br>\n")
        msg.attach(MIMEText(
            f"<html><body style='font-family:Arial,sans-serif;line-height:1.6;'>{html_body}</body></html>",
            "html",
        ))

        # ── Send via SMTP ─────────────────────────────────────────────
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=30) as server:
            if settings.SMTP_TLS:
                server.starttls()
            if settings.SMTP_USER:
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(msg)

        logger.info("Application email sent to %s for %s at %s", to_email, job_title, company)
        return True

    except smtplib.SMTPException as e:
        logger.error("SMTP error sending to %s: %s", to_email, e)
        return False
    except Exception as e:
        logger.error("Unexpected email error: %s", e)
        return False


def send_followup_email(
    to_email: str,
    to_name: str,
    job_title: str,
    company: str,
    applicant_name: str,
) -> bool:
    """
    Send a follow-up email for a previous application.

    Args:
        to_email: HR/recruiter email
        to_name: HR/recruiter name
        job_title: Job title
        company: Company name
        applicant_name: Applicant's name

    Returns:
        True if sent successfully.
    """
    if not settings.SMTP_ENABLED:
        logger.info("SMTP disabled. Would send follow-up to: %s", to_email)
        return True

    try:
        msg = MIMEText(
            f"Dear {to_name},\n\n"
            f"I am writing to follow up on my application for the {job_title} position at {company}. "
            f"I remain very interested in this opportunity and would welcome the chance to discuss "
            f"how my skills could contribute to the team.\n\n"
            f"Please let me know if there are any updates regarding my application status.\n\n"
            f"Best regards,\n{applicant_name}\n{settings.SMTP_FROM_EMAIL}"
        )
        msg["Subject"] = f"Follow-up: {job_title} application — {applicant_name}"
        msg["From"] = settings.SMTP_FROM_EMAIL
        msg["To"] = to_email

        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=30) as server:
            if settings.SMTP_TLS:
                server.starttls()
            if settings.SMTP_USER:
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(msg)

        logger.info("Follow-up email sent to %s for %s", to_email, job_title)
        return True

    except Exception as e:
        logger.error("Follow-up email error: %s", e)
        return False
