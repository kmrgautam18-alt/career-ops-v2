# Database ER Diagram

Version: 2.0

Status: Active

---

# Purpose

This document describes the actual database model for Career-Ops v2 as implemented.

The database contains **8 tables** covering users, jobs, applications, and resume data.

---

# Entity Relationship Diagram

```mermaid
erDiagram

    USERS ||--o{ JOBS : owns
    USERS ||--o{ APPLICATIONS : submits
    USERS ||--o{ RESUMES : uploads

    JOBS ||--o{ APPLICATIONS : receives

    RESUMES ||--o{ RESUME_PROFILES : has
    RESUMES ||--o{ RESUME_EXPERIENCES : has
    RESUMES ||--o{ RESUME_SKILLS : has
    RESUMES ||--o{ RESUME_EDUCATIONS : has

    USERS {
        int id PK
        string email UK
        string username UK
        string full_name
        string hashed_password
        string role
        boolean is_active
        boolean is_verified
        datetime created_at
        datetime updated_at
    }

    JOBS {
        int id PK
        int user_id FK
        string title
        string company
        string location
        string description
        string url
        string status
        datetime created_at
        datetime updated_at
    }

    APPLICATIONS {
        int id PK
        int user_id FK
        int job_id FK
        string status
        text notes
        datetime created_at
        datetime updated_at
    }

    RESUMES {
        int id PK
        int user_id FK
        string file_name
        string file_type
        int file_size
        string file_path
        string status
        datetime created_at
        datetime updated_at
    }

    RESUME_PROFILES {
        int id PK
        int resume_id FK
        string name
        string email
        string phone
        string location
        text summary
        float confidence
        datetime created_at
    }

    RESUME_EXPERIENCES {
        int id PK
        int resume_id FK
        string company
        string designation
        string location
        date start_date
        date end_date
        boolean is_current
        string employment_type
        text description
        float confidence
        datetime created_at
    }

    RESUME_SKILLS {
        int id PK
        int resume_id FK
        string skill_name
        string category
        float confidence
        datetime created_at
    }

    RESUME_EDUCATIONS {
        int id PK
        int resume_id FK
        string degree
        string specialization
        string institution
        string location
        string university
        date start_date
        date end_date
        float grade
        float percentage
        float cgpa
        boolean currently_studying
        float confidence
        datetime created_at
    }
```

---

# Table Relationships

```
users
 ├──< jobs          (one user has many jobs)
 ├──< applications  (one user has many applications)
 └──< resumes       (one user has many resumes)

jobs
 └──< applications  (one job can have many applications)

resumes
 ├──< resume_profiles      (one resume has one profile)
 ├──< resume_experiences   (one resume has many experiences)
 ├──< resume_skills        (one resume has many skills)
 └──< resume_educations    (one resume has many educations)
```

---

# Key Design Decisions

| Decision | Implementation |
|----------|---------------|
| Primary keys | Auto-increment integers (UUID planned for future) |
| Foreign keys | Cascading deletes (CASCADE on resume child tables) |
| Timestamps | All tables have `created_at`, most have `updated_at` |
| Soft deletes | Not yet implemented (planned) |
| Indexed columns | `email`, `username`, `user_id`, `resume_id`, `job_id` |
| Search columns | `title`, `company`, `status`, `degree` are indexed |

---

# Migration Management

- Managed via **Alembic** with versioned migration scripts
- Current schema version: 7 migrations applied
- Supports both SQLite (dev) and PostgreSQL (prod)
- Migrations located in `alembic/versions/`

---

# Design Principles

- Normalized schema with foreign key constraints
- All user data is scoped by `user_id`
- Resume data is decomposed into structured entities (profile, experience, skill, education)
- AI-ready schema — confidence scores stored alongside extracted data
- Future: UUID primary keys, soft deletes, audit logging
