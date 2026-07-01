"""
File upload configuration.

This module centralizes all file upload related constants.
"""

from pathlib import Path

# ==========================================================
# Resume Upload
# ==========================================================

# Maximum allowed resume size (5 MB)
MAX_RESUME_SIZE_MB = 5

MAX_RESUME_SIZE_BYTES = MAX_RESUME_SIZE_MB * 1024 * 1024


# ==========================================================
# Allowed MIME Types
# ==========================================================

ALLOWED_RESUME_TYPES = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}


# ==========================================================
# Allowed File Extensions
# ==========================================================

ALLOWED_RESUME_EXTENSIONS = {
    ".pdf",
    ".docx",
}


# ==========================================================
# Storage Directories
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[3]

STORAGE_DIR = PROJECT_ROOT / "storage"

RESUME_STORAGE_DIR = STORAGE_DIR / "resumes"


# ==========================================================
# UUID Filename
# ==========================================================

UUID_FILENAME_LENGTH = 36