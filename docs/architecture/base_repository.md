# Base Repository

## Purpose

Provide common repository functionality for all database repositories.

## Responsibilities

- Database session
- Commit
- Rollback
- Flush
- Refresh
- Generic CRUD
- Transaction management
- Logging

## Design Principles

- Reusable
- Type-safe
- Framework independent
- Easy to extend
- Enterprise ready

## Child Repositories

- ResumeRepository
- ResumeProfileRepository
- ResumeSkillRepository
- JobRepository
- ApplicationRepository
- InterviewRepository
- EducationRepository
- ExperienceRepository

## Current Implementations

- ResumeProfileRepository
- ResumeSkillRepository (In Progress)

All repositories inherit from BaseRepository and use its transaction helpers instead of directly calling:

- db.add()
- db.commit()
- db.rollback()
- db.refresh()