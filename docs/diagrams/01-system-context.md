# System Context Diagram

Version: 1.0

Status: Active

---

# Purpose

This diagram shows the highest-level view of Career-Ops v2 and its interaction with external users and systems.

---

## System Context

```mermaid
flowchart TD

    User["👤 Candidate / Recruiter"]

    Browser["🌐 Web Browser"]

    CareerOps["🚀 Career-Ops v2"]

    AI["🤖 AI Providers
(OpenAI / Gemini / Claude)"]

    JobSites["💼 Job Portals
(LinkedIn / Indeed / Company Careers)"]

    GitHub["🐙 GitHub"]

    Email["📧 Email"]

    Telegram["📱 Telegram"]

    PostgreSQL["🗄 PostgreSQL"]

    n8n["⚡ n8n Automation"]

    User --> Browser

    Browser --> CareerOps

    CareerOps --> AI

    CareerOps --> PostgreSQL

    CareerOps --> n8n

    CareerOps --> GitHub

    CareerOps --> JobSites

    n8n --> Email

    n8n --> Telegram
```

---

# External Actors

## Candidate

- Searches jobs
- Uploads resumes
- Tracks applications
- Receives interview preparation

---

## Recruiter

- Reviews candidate profiles
- Searches applicants
- Views analytics

---

## External Systems

### AI Providers

Responsible for:

- Resume Optimization
- ATS Analysis
- Job Matching
- Interview Coaching

---

### Job Portals

Responsible for:

- Job Discovery
- Job Import
- Future Auto Apply

---

### GitHub

Responsible for:

- Source Code
- CI/CD
- Version Control

---

### n8n

Responsible for:

- Workflow Automation
- Notifications
- Scheduled Jobs

---

# Goal

Career-Ops v2 acts as the central platform connecting users, AI providers, automation services, databases, and external job portals into one integrated career management ecosystem.