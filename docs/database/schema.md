# Database Schema

| Field           | Value           |
| --------------- | --------------- |
| Document        | Database Schema |
| Version         | 1.0             |
| Status          | Draft           |
| Project Version | v0.2.0          |
| Last Updated    | 2026-06-27      |
| Owner           | KUMAR GAUTAM    |

---

# Purpose

This document describes the database design of Career-Ops v2.

It explains the current database implementation, table structures, relationships, and the planned migration from SQLite to PostgreSQL.

The goal is to maintain a scalable, maintainable, and production-ready database architecture.

---

# Current Database

The current version of Career-Ops v2 uses **SQLite** as the primary database.

SQLite was selected during the initial development phase because it:

* Requires no separate database server
* Is lightweight and easy to configure
* Supports rapid application development
* Integrates seamlessly with SQLAlchemy ORM
* Is ideal for local development and testing

The application currently stores:

* Jobs
* Applications
* Resumes
* Interviews

Future releases will migrate the application to PostgreSQL for production deployment.

---

# Current Tables

The current database consists of the following tables.

| Table        | Purpose                                          |
| ------------ | ------------------------------------------------ |
| jobs         | Stores job postings collected by the application |
| applications | Stores job application records                   |
| resumes      | Stores uploaded resume information               |
| interviews   | Stores interview schedules and outcomes          |

These tables represent the first version of the Career-Ops data model.

Additional tables will be introduced in future versions as new features are implemented.

---

# Table Relationships

The current database uses the following relationships:

```text
jobs
 │
 └───────< applications
              │
              └──────< interviews

resumes
```

Relationship Summary

* One Job can have multiple Applications.
* One Application can have multiple Interviews.
* Resume information is currently stored independently.
* Future releases will associate resumes with applications and users.

