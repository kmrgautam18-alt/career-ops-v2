# Career-Ops v2 Master Architecture

Version: 2.0
Status: Active (Production Ready)
Last Updated: 2026-07-16

---

## 🎯 Vision

Career-Ops v2 is an enterprise-grade AI-powered Career Operating System that combines Backend Engineering, DevOps, Artificial Intelligence, Automation, and Cloud Native technologies into a single production-ready platform.

---

## ✅ Current Status — All Phases Complete

| Phase | Status | Components |
|-------|:------:|------------|
| Foundation | ✅ | FastAPI, SQLAlchemy, Pydantic, Layered Architecture |
| Authentication | ✅ | JWT + Argon2 + RBAC + Refresh Tokens |
| PostgreSQL Migration | ✅ | SQLAlchemy + Alembic, Pooled Connections |
| Testing | ✅ | 115 tests (98 existing + 17 webhook tests) |
| Docker | ✅ | 13 services, multi-stage builds |
| CI/CD | ✅ | GitHub Actions ready, deploy scripts |
| Monitoring | ✅ | Prometheus + Grafana + Alertmanager |
| AI Platform | ✅ | Gemini-powered ATS, Interviews, Optimizer, Job Match — all with streaming SSE |
| Automation | ✅ | n8n with 3 pre-built workflows, webhook triggers |
| Frontend | ✅ | 8 pages, dark luxury theme, Framer Motion animations |
| Production Release | ✅ | Deployment guides for RHEL and AWS EC2 |

---

## 🏗️ System Architecture (Current)

### High-Level Overview

```
                    ┌──────────────────────────────────────────────────┐
                    │                 Internet                         │
                    │           (https://your-domain.com)               │
                    └──────────────────────┬───────────────────────────┘
                                           │
                                           ▼
                    ┌──────────────────────────────────────────────────┐
                    │              Nginx (port 80/443)                  │
                    │         SPA static files + /api/* proxy           │
                    │         stub_status for nginx-exporter            │
                    └──────────────────────┬───────────────────────────┘
                                           │
                      ┌────────────────────┼────────────────────┐
                      │                    │                    │
                      ▼                    ▼                    ▼
              ┌──────────────┐    ┌──────────────┐    ┌──────────────────┐
              │ 🚀 FastAPI   │    │ ⚛️ React SPA │    │ 🔔 Alertmanager  │
              │   :8000      │    │   (built)    │    │   :9093           │
              │   /metrics   │    └──────────────┘    └──────────────────┘
              └──────┬───────┘
                     │
         ┌───────────┼───────────┐
         ▼           ▼           ▼
   ┌──────────┐ ┌────────┐ ┌──────────┐
   │PostgreSQL│ │ Gemini │ │  n8n    │
   │  :5432   │ │  AI    │ │ :5678   │
   └──────────┘ └────────┘ └──────────┘
                                       │
                                ┌──────┴──────┐
                                │ 3 Workflows │
                                │ Job Alerts  │
                                │ Status Email│
                                │ Daily Digest│
                                └─────────────┘
```

### Monitoring & Logging Stack

```
                        ┌───────────────────────┐
                        │      Grafana :3001      │
                        │ Prometheus + Loki DS    │
                        │ 12-panel dashboard      │
                        └────┬──────────┬─────────┘
                             │          │
                     ┌───────▼──┐  ┌────▼──────┐
                     │Prometheus│  │   Loki    │
                     │  :9090   │  │  :3100    │
                     └──┬───┬───┘  └────┬──────┘
                        │   │           │
              ┌─────────┘   └────┐  ┌──┴─────┐
              ▼                  ▼  │Promtail│
        ┌──────────┐     ┌────────┐ └────────┘
        │ Postgres │     │ Nginx  │
        │ Exporter │     │Exporter│
        │  :9187   │     │ :9113  │
        └──────────┘     └────────┘
```

### Alerting Pipeline

```
Prometheus ──(fires alert)──▶ Alertmanager ──▶ Slack Webhook
                    │                        ├── PagerDuty
                    │                        └── Email
                    │
                    ▼
            14 Alert Rules:
            Backend Down (critical)
            High Error Rate (critical)
            Postgres Down (critical)
            Disk Space Low (critical)
            Nginx Down (critical)
            High Latency (warning)
            Slow DB Queries (warning)
            High AI Latency (warning)
            No New Users (info)
            ... and 5 more
```

---

## 🧩 All 13 Docker Services

| # | Service | Image | Port | Purpose |
|---|---------|-------|:----:|---------|
| 1 | **PostgreSQL** | `postgres:16-alpine` | `:5432` | Production database |
| 2 | **Backend** | Custom multi-stage build | `:8000` | FastAPI + AI engine + `/metrics` |
| 3 | **Frontend** | Custom Bun → Nginx build | `:80` | React SPA with proxy |
| 4 | **Prometheus** | `prom/prometheus:v3.2.1` | `:9090` | Metrics + alert evaluation |
| 5 | **Grafana** | `grafana/grafana:11.6.0` | `:3001` | Dashboards + explore |
| 6 | **Alertmanager** | `prom/alertmanager:v0.28.1` | `:9093` | Alert routing & dedup |
| 7 | **Loki** | `grafana/loki:3.4.2` | `:3100` | Log aggregation |
| 8 | **Promtail** | `grafana/promtail:3.4.2` | — | Docker log scraping |
| 9 | **Postgres Exporter** | `prometheuscommunity/postgres-exporter:v0.17.1` | `:9187` | DB metrics |
| 10 | **Nginx Exporter** | `nginx/nginx-prometheus-exporter:1.5.0` | `:9113` | Web server metrics |
| 11 | **n8n** | `n8nio/n8n:1.88.0` | `:5678` | Workflow automation |
| 12 | **Postgres Exporter** (duplicate) | — | — | — |
| 13 | **(n8n workflows)** | Pre-built JSON imports | — | Job alerts, status email, daily digest |

---

## 🎨 Frontend Architecture

```
React 19 + Vite 8 + TypeScript 6 + Tailwind CSS 4 + Framer Motion
                        │
          ┌─────────────┼──────────────┐
          ▼             ▼              ▼
    ┌──────────┐ ┌──────────┐ ┌──────────────┐
    │  Auth    │ │ Dashboard│ │   Pages      │
    │ Context  │ │ Layout   │ │ Landing      │
    │          │ │ Sidebar  │ │ Login/Reg    │
    │          │ │ Theme    │ │ Dashboard    │
    │          │ │ Toggle   │ │ Jobs         │
    │          │ │ Skel.    │ │ Apps         │
    │          │ │ Loading  │ │ Resumes      │
    │          │ │ Anim.    │ │ AI Tools     │
    └──────────┘ └──────────┘ └──────────────┘
```

### Frontend Features
- Dark Luxury / Metallic Light theme toggle
- Direction-aware page transitions (left/right slide based on nav direction)
- Loading skeletons per page (Dashboard, Jobs, Apps, Resumes, AI)
- Avatar trail animation in sidebar during navigation
- Streaming SSE support for all 4 AI tools (ATS, Interviews, Optimizer, Job Match)
- Framer Motion `layoutId` animations for tab switching

---

## 🤖 AI Architecture

```
Frontend ──POST /ai/*──▶ FastAPI ──▶ LLM Service ──▶ Google Gemini API
                                    │
                           ┌────────┴────────┐
                           │                 │
                    ┌───────────┐   ┌──────────────┐
                    │ Streaming  │   │ Batch (JSON) │
                    │ SSE Events │   │ Full Response│
                    └───────────┘   └──────────────┘
                                    │
                    ┌───────────────┼────────────────┐
                    ▼               ▼                ▼
              ┌──────────┐  ┌────────────┐  ┌──────────────┐
              │ ATS Score │  │ Interview  │  │    Resume    │
              │ + Job     │  │ Questions  │  │  Optimizer   │
              │  Match    │  │ 8 per role │  │ Before/After │
              └──────────┘  └────────────┘  └──────────────┘
```

### Fallback Strategy
If `LLM_API_KEY` is not set, the system gracefully falls back to **rule-based engines** for all AI features.

---

## 🔗 Backend → n8n Webhooks

```
Application Created ──▶ POST /webhook/careerops-application-created
Application Updated ──▶ POST /webhook/careerops-application-status
Application Deleted ──▶ POST /webhook/careerops-application-deleted

Each webhook sends: { user_email, company, job_title, status, previous_status, ... }
```

---

## 📦 Project Structure

```
.
├── backend/app/          # FastAPI + SQLAlchemy + Pydantic
│   ├── api/v1/           # 12 route modules (auth, users, jobs, apps, resumes, AI, admin, etc.)
│   ├── core/             # Config with all env vars
│   ├── services/         # Business logic + AI + Webhooks
│   ├── models/           # 8 SQLAlchemy ORM models
│   ├── schemas/          # Pydantic request/response schemas
│   └── main.py           # App entry + /metrics endpoint
├── frontend/             # React 19 + Vite 8 + TypeScript 6
│   └── src/
│       ├── api/          # Axios client with SSE streaming
│       ├── components/   # Layout, Sidebar, ThemeToggle, Skeleton
│       ├── context/      # AuthContext, ThemeContext
│       └── pages/        # 8 pages with Framer Motion
├── monitoring/           # Full observability stack
│   ├── prometheus.yml     # 5 scrape jobs
│   ├── prometheus-rules.yml # 14 alerting rules
│   ├── alertmanager/      # Slack, PagerDuty, Email config
│   ├── grafana/           # Auto-provisioned datasources + dashboard
│   ├── loki/              # Loki + Promtail config
│   └── n8n/workflows/     # 3 pre-built workflow JSONs
├── docs/                  # 40+ docs, 17 diagrams, 3 deployment guides
├── tests/                 # 115 tests (pytest)
├── docker-compose.yml     # 13 services
├── Dockerfile             # Multi-stage backend build
└── README.md              # Full project documentation
```

---

## 🔐 Security Architecture

| Layer | Technology | Status |
|-------|-----------|:------:|
| Authentication | JWT (python-jose) + Argon2 | ✅ |
| Authorization | Role-Based Access Control (RBAC) | ✅ |
| Token Refresh | Refresh tokens with 7-day expiry | ✅ |
| CORS | Configurable origins (dev/prod) | ✅ |
| Secrets | Environment variables, .env in .gitignore | ✅ |
| HTTPS | Let's Encrypt + Certbot (production) | ✅ |
| Input Validation | Pydantic schemas | ✅ |

---

## 📈 Observability

| Component | What It Monitors | Retention |
|-----------|-----------------|:---------:|
| Prometheus | 15+ metric types (HTTP, DB, AI, business) | 30 days |
| Grafana | 12-panel dashboard (auto-provisioned) | — |
| Loki | All Docker container logs | 7 days |
| Alertmanager | 14 alerting rules → Slack/PD/Email | — |
| Backend `/metrics` | Prometheus exposition format | — |

---

## 🚀 Deployment Options

| Platform | Guide | Services |
|----------|-------|:--------:|
| 🖥️ **RHEL 10.2** | [`docs/deployment/rhel-vm-deployment.md`](../deployment/rhel-vm-deployment.md) | 13 |
| ☁️ **AWS EC2** | [`docs/deployment/aws-ec2-deployment.md`](../deployment/aws-ec2-deployment.md) | 13 |
| 🌐 **RHEL Go-Live** (public internet) | [`docs/deployment/rhel-go-live-guide.md`](../deployment/rhel-go-live-guide.md) | 13 + HTTPS + DNS |

---

## 📊 Project Stats

| Metric | Value |
|--------|:-----:|
| Backend API Endpoints | 134 |
| Backend Tests | 115 passing |
| Frontend Pages | 8 |
| Frontend TypeScript | Zero errors |
| Docker Services | 13 |
| Monitoring Alert Rules | 14 |
| Grafana Dashboard Panels | 12 |
| Deployment Guides | 3 |
| Documentation Files | 40+ |
| Architecture Diagrams | 17 |
