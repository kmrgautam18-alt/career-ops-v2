"""
ATS scoring configuration.
"""

# Weightage (must total 100)
KEYWORD_WEIGHT = 40
FORMATTING_WEIGHT = 20
SECTION_WEIGHT = 20
READABILITY_WEIGHT = 20

TOTAL_WEIGHT = (
    KEYWORD_WEIGHT
    + FORMATTING_WEIGHT
    + SECTION_WEIGHT
    + READABILITY_WEIGHT
)

# Expected resume sections
REQUIRED_SECTIONS = [
    "summary",
    "experience",
    "education",
    "skills",
]

# ATS-friendly file formats
SUPPORTED_FORMATS = {
    ".pdf",
    ".docx",
}

# Common ATS keywords
IMPORTANT_KEYWORDS = [
    "python",
    "docker",
    "kubernetes",
    "linux",
    "aws",
    "azure",
    "terraform",
    "ansible",
    "git",
    "ci/cd",
]