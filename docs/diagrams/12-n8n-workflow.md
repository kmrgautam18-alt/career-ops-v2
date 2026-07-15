# n8n Workflow Automation

Version: 1.0

Status: Planned

---

# Purpose

This diagram illustrates planned workflow automation patterns using n8n to extend Career-Ops v2 capabilities with email notifications, job discovery, and scheduled tasks.

---

# Automation Architecture

```mermaid
flowchart TD

    CareerOps["🚀 Career-Ops API"]
    n8n["⚡ n8n Automation Server"]
    Scheduler["⏰ Scheduler\nCron Triggers"]
    Webhook["🔗 Webhook\nEvent Triggers"]

    subgraph Channels["📨 Notification Channels"]
        Email["📧 Email\nSMTP / SendGrid"]
        Telegram["📱 Telegram Bot"]
    end

    subgraph Actions["⚙️ Automated Actions"]
        JobDiscovery["💼 Job Discovery\nScrape job boards"]
        ResumeAnalysis["📄 Resume Analysis\nPeriodic ATS check"]
        FollowUp["📞 Follow-up Reminders\nApplication status"]
        InterviewPrep["🎤 Interview Prep\nAuto-generate questions"]
    end

    subgraph Triggers["🔔 Trigger Sources"]
        NewJob["New Job Added"]
        StatusChange["Application Status Change"]
        WeeklyDigest["Weekly Schedule"]
        UpcomingInterview["Interview Scheduled"]
    end

    NewJob --> Webhook
    StatusChange --> Webhook
    WeeklyDigest --> Scheduler
    UpcomingInterview --> Webhook

    Webhook --> n8n
    Scheduler --> n8n
    n8n --> CareerOps

    n8n --> JobDiscovery
    n8n --> ResumeAnalysis
    n8n --> FollowUp
    n8n --> InterviewPrep

    JobDiscovery --> Email
    FollowUp --> Telegram
    InterviewPrep --> Email
    ResumeAnalysis --> Email
```

---

# Example Workflows

## 1. Application Follow-up Reminder

```mermaid
sequenceDiagram

    participant n8n as n8n
    participant API as Career-Ops API
    participant Scheduler as Cron (7 days)
    participant Email as Email Service
    participant User as User

    Scheduler->>n8n: Every Sunday at 9 AM
    n8n->>API: GET /api/v1/applications?status=applied
    API-->>n8n: [application1, application2, ...]
    
    n8n->>n8n: Filter applications older than 7 days
    n8n->>API: GET /api/v1/users/me
    API-->>n8n: user@email.com
    
    n8n->>Email: Send follow-up reminder
    Email-->>User: "⏰ Follow up on Senior Engineer at Google (applied 8 days ago)"
```

## 2. Weekly Job Search Digest

```mermaid
sequenceDiagram

    participant n8n as n8n
    participant API as Career-Ops API
    participant AI as AI Engine
    participant Scheduler as Cron (Weekly)
    participant Email as Email Service

    Scheduler->>n8n: Every Monday at 8 AM
    n8n->>API: GET /api/v1/dashboard/status-summary
    API-->>n8n: {applied: 5, interviews: 2, rejected: 1}
    
    n8n->>API: GET /api/v1/dashboard/recent-jobs
    API-->>n8n: [job1, job2, ...]
    
    n8n->>Email: Send weekly digest
    Email-->>Email: "📊 Your Weekly Career Summary"
```

---

# Planned Webhook Endpoints

| Endpoint | Trigger | Payload |
|----------|---------|---------|
| `POST /api/v1/webhooks/job-created` | New job saved | `{job_id, title, company}` |
| `POST /api/v1/webhooks/application-updated` | Status change | `{app_id, from_status, to_status}` |
| `POST /api/v1/webhooks/interview-scheduled` | New interview | `{app_id, date, round}` |

---

# n8n Integration Status

| Feature | Status |
|---------|:------:|
| Career-Ops REST API | ✅ Ready to consume |
| Webhook endpoints | 🔜 Planned |
| n8n server setup | 🔜 Planned |
| Email notifications | 🔜 Planned |
| Telegram notifications | 🔜 Planned |
| Weekly digest | 🔜 Planned |
| Auto follow-up reminders | 🔜 Planned |
| Automated job discovery | 🔜 Planned |
