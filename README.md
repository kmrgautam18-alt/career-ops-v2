<div align="center">
  <br/>
  <img src="https://img.shields.io/badge/status-active-success.svg" alt="Status" />
  <img src="https://img.shields.io/badge/tests-98%25-passing-success" alt="Tests" />
  <img src="https://img.shields.io/badge/license-MIT-blue" alt="License" />
  <img src="https://img.shields.io/badge/python-3.12-blue" alt="Python" />
  <img src="https://img.shields.io/badge/react-19-61DAFB" alt="React" />
  <br/><br/>
</div>

# 🚀 Career-Ops v2

**AI-Powered Career Operating System** — a unified platform that helps professionals manage their entire career lifecycle: resumes, job applications, interview preparation, career analytics, and AI-powered career guidance.

---

## ✨ Features

### 🎯 Job Management
- Full CRUD for job opportunities with search, filtering, and sorting
- Track job sources, statuses, and deadlines
- AI-powered job matching against your resume

### 📄 Resume Intelligence
- Upload and manage multiple resumes (PDF, DOCX)
- AI-powered resume parsing and analysis
- ATS (Applicant Tracking System) scoring
- Resume optimization recommendations

### 📋 Application Tracking
- Track every stage of your job applications
- Status management: Saved → Applied → Interview → Offer → Accepted/Rejected
- Interview scheduling and outcome tracking
- Notes and history for each application

### 🤖 AI Career Assistant
- **ATS Score Calculator** — Analyze your resume against any job description
- **Interview Question Generator** — Generate role-specific practice questions
- **Resume Optimizer** — Get AI-powered suggestions to improve your resume
- **Career Analytics** — Track your progress with data-driven insights

### 📊 Dashboard & Analytics
- Real-time overview of your career metrics
- Recent jobs and applications at a glance
- Status summaries and trend tracking

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   Frontend (React + Vite)                    │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌───────────────┐  │
│  │  Auth    │ │Dashboard │ │   Jobs   │ │  AI Tools     │  │
│  │  Pages   │ │  Stats   │ │ Manager  │ │  (ATS, Inter) │  │
│  └──────────┘ └──────────┘ └──────────┘ └───────────────┘  │
│                        │ Axios (JWT)                        │
├────────────────────────┼────────────────────────────────────┤
│           Backend (FastAPI + Python 3.12)                    │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌───────────────┐  │
│  │  Router  │ │  Service │ │Repository│ │   Security    │  │
│  │  Layer   │→│  Layer   │→│  Layer   │ │  (JWT Auth)   │  │
│  └──────────┘ └──────────┘ └──────────┘ └───────────────┘  │
│                        │ SQLAlchemy                          │
├────────────────────────┼────────────────────────────────────┤
│        Database (SQLite Dev / PostgreSQL Prod)               │
└─────────────────────────────────────────────────────────────┘
```

### Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | React 19, TypeScript 6, Vite 8, Tailwind CSS 4, Framer Motion, Recharts |
| **Backend** | Python 3.12, FastAPI, SQLAlchemy 2.0, Pydantic 2 |
| **Database** | SQLite (dev), PostgreSQL 16 (prod), Alembic migrations |
| **Auth** | JWT (python-jose) — access + refresh tokens, Argon2 password hashing |
| **AI** | Custom ATS engine, Interview question generator, Resume optimizer |
| **Deployment** | Docker, Docker Compose, Nginx, AWS EC2 |

### Project Structure

```
.
├── backend/
│   └── app/
│       ├── api/v1/           # 10 route modules (auth, jobs, resumes, ai, baserow...)
│       ├── core/             # Config, settings
│       ├── database/         # Engine, session, migrations
│       ├── models/           # 8 SQLAlchemy ORM models
│       ├── schemas/          # Pydantic request/response schemas
│       ├── services/         # Business logic (AI, extraction, matching, baserow)
│       ├── repositories/     # Data access layer
│       ├── security/         # JWT, password hashing
│       ├── knowledge/        # Resume/skill extraction engines
│       ├── resources/        # Knowledge base text files
│       └── main.py           # FastAPI app entry point
├── frontend/
│   └── src/
│       ├── api/              # Axios client with JWT interceptors
│       ├── components/       # Layout, Sidebar, ProtectedRoute
│       ├── context/          # AuthContext
│       └── pages/            # Landing, Login, Register, Dashboard, Jobs, Apps, Resumes, AI
├── docs/                     # Architecture docs, blueprints, diagrams
├── scripts/                  # EC2 bootstrap, deploy helper
├── tests/                    # 98 Pytest tests
├── .claude/                  # Claude Code project settings
├── Dockerfile                # Multi-stage backend build
├── frontend/Dockerfile       # Frontend Nginx build
├── frontend/nginx.conf       # Nginx config (SPA + API proxy)
├── docker-compose.yml        # PostgreSQL + Backend + Frontend
└── .env.example              # All environment variables
```

---

## 🚀 Quick Start (Local Development)

### Prerequisites
- Python 3.12+
- Bun (or Node.js 22+)
- Git

### Backend

```bash
# Clone and enter
git clone https://github.com/kmrgautam18-alt/career-ops-v2.git
cd career-ops-v2

# Install Python deps
pip install -r requirements.txt

# Create data directory
mkdir -p data

# Start the dev server
DATABASE_URL='sqlite:///./data/careerops.db' \
SECRET_KEY='dev-secret-change-in-production' \
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend

```bash
# In a separate terminal
cd frontend

# Install JS deps
bun install

# Start the dev server (proxies /api to backend)
bun dev
```

The frontend opens at **http://localhost:5173** and the API at **http://localhost:8000**.

---

## 📖 API Reference

The full OpenAPI/Swagger docs are available at **`http://localhost:8000/docs`** when the server is running.

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/login` | Sign in (returns JWT) |
| POST | `/api/v1/auth/refresh` | Refresh access token |
| POST | `/api/v1/auth/logout` | Sign out |
| POST | `/api/v1/users/register` | Create account |
| GET | `/api/v1/users/me` | Current user profile |

### Core Resources

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/api/v1/jobs` | List / Create jobs |
| GET/PATCH/DELETE | `/api/v1/jobs/{id}` | Get / Update / Delete job |
| POST | `/api/v1/jobs/{id}/match/{resume_id}` | Match job with resume |
| GET/POST | `/api/v1/applications` | List / Create applications |
| GET/PATCH/DELETE | `/api/v1/applications/{id}` | Get / Update / Delete |
| GET/POST | `/api/v1/resumes` | List / Upload resumes |
| GET/PATCH/DELETE | `/api/v1/resumes/{id}` | Get / Update / Delete resume |

### Dashboard & AI

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/dashboard/` | Overview stats |
| GET | `/api/v1/dashboard/status-summary` | Status breakdown |
| POST | `/api/v1/ai/ats-score` | Calculate ATS compatibility |
| POST | `/api/v1/ai/interview/questions` | Generate interview questions |
| POST | `/api/v1/ai/resume-optimize` | Optimize resume text |

### Integrations

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/baserow/health` | Check Baserow connection |
| GET/POST | `/api/v1/baserow/tables/{id}/rows` | Baserow row CRUD |
| GET | `/api/v1/baserow/tables/{db_id}` | List Baserow tables |

---

## 🐳 Production Deployment (Docker)

```bash
# 1. Set up environment
cp .env.example .env
# Edit .env with your production values

# 2. Start the full stack
docker compose up -d --build

# 3. Run database migrations
docker compose exec backend alembic upgrade head

# 4. Verify
curl http://localhost/
# → {"application":"Career-Ops v2","status":"healthy"}
```

### AWS EC2 Deployment

```bash
# One-time: Bootstrap an Ubuntu 24.04 EC2 instance
# (uses scripts/ec2-bootstrap.sh)

# Updates: Deploy from your machine
EC2_HOST="ec2-xx-xx-xx-xx.compute-1.amazonaws.com" \
EC2_SSH_KEY="~/.ssh/your-key.pem" \
bash scripts/deploy-ec2.sh
```

See [scripts/setup-ec2-instance.md](scripts/setup-ec2-instance.md) for the complete guide.

---

## 🧪 Testing

```bash
# Run all 98 backend tests
python3 -m pytest tests/ -q

# Frontend typecheck
cd frontend && bun tsc -b --noEmit

# Frontend production build
cd frontend && bun run build
```

---

## 🔧 Environment Variables

| Variable | Default | Required | Description |
|----------|---------|----------|-------------|
| `DATABASE_URL` | `sqlite:///data/careerops.db` | ✅ | Database connection string |
| `SECRET_KEY` | `change-this-secret-key` | ✅ | JWT signing secret |
| `CORS_ORIGINS` | `http://localhost:5173,...` | ✅ | Allowed CORS origins |
| `BASEROW_URL` | `https://api.baserow.io` | ⬜ | Baserow instance URL |
| `BASEROW_TOKEN` | — | ⬜ | Baserow API token |
| `ANTHROPIC_API_KEY` | — | ⬜ | Claude Code API key |
| `POSTGRES_PASSWORD` | — | ⬜ | PostgreSQL password (Docker) |

Full list in [.env.example](.env.example)

---

## 🧠 Integrations

- **Baserow** — No-code database / Airtable alternative for collaborative data management
- **Claude Code** — AI coding assistant pre-configured with project context via `CLAUDE.md`
- **AWS EC2** — Deployment target with automated bootstrap and deploy scripts

---

## 📊 Project Status

| Area | Status |
|------|--------|
| Backend API | ✅ Complete (134 endpoints, 8 modules) |
| Frontend UI | ✅ Complete (8 pages, dark theme, responsive) |
| Auth (JWT) | ✅ Working (register, login, refresh, logout) |
| AI Features | ✅ Working (ATS scoring, interview questions) |
| Database | ✅ SQLite (dev) / PostgreSQL (prod) |
| Tests | ✅ 98/98 passing |
| Docker | ✅ Multi-service compose (PostgreSQL + Backend + Nginx) |
| EC2 Deployment | ✅ Automated bootstrap & deploy scripts |
| Baserow | ✅ Integrated (REST API client, 7 endpoints) |
| Claude Code | ✅ Configured (CLAUDE.md, .claude/settings.json) |

---

## 📚 Documentation

Detailed documentation is available in the [docs/](docs/) directory:

- [Project Vision](docs/blueprint/BP-001_PROJECT_VISION.md)
- [Business Requirements](docs/blueprint/BP-002_BUSINESS_REQUIREMENTS.md)
- [System Architecture](docs/architecture/system-architecture.md)
- [Backend Architecture](docs/architecture/backend-architecture.md)
- [Database Schema](docs/database/schema.md)
- [API Authentication](docs/api/authentication.md)
- [Deployment Guide](scripts/setup-ec2-instance.md)

---

## 👤 Author

**Kumar Gautam**

---

## 📄 License

This project is open source and available under the MIT License.
