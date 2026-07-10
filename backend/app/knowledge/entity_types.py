from enum import Enum


class EntityType(str, Enum):
    """
    Universal entity types used throughout Career-Ops.
    """

    PERSON = "person"

    EMAIL = "email"

    PHONE = "phone"

    LOCATION = "location"

    WEBSITE = "website"

    LINKEDIN = "linkedin"

    GITHUB = "github"

    PORTFOLIO = "portfolio"

    SKILL = "skill"

    TOOL = "tool"

    TECHNOLOGY = "technology"

    FRAMEWORK = "framework"

    LIBRARY = "library"

    PROGRAMMING_LANGUAGE = "programming_language"

    CLOUD_PLATFORM = "cloud_platform"

    DATABASE = "database"

    OPERATING_SYSTEM = "operating_system"

    CERTIFICATION = "certification"

    DEGREE = "degree"

    EDUCATION = "education"

    COMPANY = "company"

    DESIGNATION = "designation"

    PROJECT = "project"

    DOMAIN = "domain"

    INDUSTRY = "industry"

    RESPONSIBILITY = "responsibility"

    ACHIEVEMENT = "achievement"

    UNKNOWN = "unknown"