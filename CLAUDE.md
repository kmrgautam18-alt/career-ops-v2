# Career-Ops v2 — Project Guide for Claude Code

## Overview
Career-Ops is an AI-powered Career Operating System with a Python FastAPI backend and React + Vite + TypeScript frontend. It helps professionals manage resumes, job applications, interviews, and career analytics.

## Tech Stack
- **Backend:** Python 3.12, FastAPI, SQLAlchemy 2.0, SQLite (dev) / PostgreSQL (prod)
- **Frontend:** React 19, TypeScript 6, Vite 8, Tailwind CSS 4, Framer Motion, Recharts
- **Database:** SQLAlchemy ORM with Alembic migrations
- **Auth:** JWT (python-jose) with access + refresh tokens
- **AI:** ATS scoring, resume optimization, interview question generation
- **Deployment:** Docker Compose with PostgreSQL + Nginx

## Project Structure
```
.
├── backend/
│   └── app/
│       ├── api/v1/        # FastAPI route handlers
│       ├── core/          # Config, settings
│       ├── database/      # Engine, session, init_db, base
│       ├── models/        # SQLAlchemy ORM models
│       ├── schemas/       # Pydantic request/response schemas
│       ├── services/      # Business logic (AI, extraction, matching)
│       ├── repositories/  # Data access layer
│       ├── security/      # JWT, password hashing, auth deps
│       ├── knowledge/     # Resume/skill extraction engines
│       └── main.py        # FastAPI app entry point
├── frontend/
│   └── src/
│       ├── api/           # Axios client + API service functions
│       ├── components/    # Layout, Sidebar, ProtectedRoute
│       ├── context/       # AuthContext (React context)
│       └── pages/         # Auth, Dashboard, Jobs, Applications, Resumes, AI
├── docs/                  # Architecture, blueprint, diagrams
├── scripts/               # EC2 bootstrap, deploy helper
├── tests/                 # Pytest test suite (98 passing)
├── Dockerfile             # Backend multi-stage build
├── docker-compose.yml     # PostgreSQL + Backend + Nginx
└── .env.example           # Production env template
```

## Key Commands
```bash
# Backend
pip install -r requirements.txt               # Install deps
DATABASE_URL='sqlite:///./data/careerops.db' uvicorn backend.app.main:app --reload  # Dev server
python3 -m pytest tests/ -q                   # Run tests (98 pass)

# Frontend
cd frontend && bun install                    # Install deps
cd frontend && bun dev                        # Dev server (port 5173)
cd frontend && bun tsc -b --noEmit            # Typecheck
cd frontend && bun run build                  # Production build

# Database
alembic upgrade head                          # Run migrations
python3 -c "from backend.app.database.init_db import init_database; init_database()"  # Create tables

# Deploy
docker compose up -d --build                  # Full stack
bash scripts/deploy-ec2.sh                    # Deploy to EC2
```

## Architecture Patterns
- **Layered:** Router → Service → Repository → ORM → Database
- **Auth:** JWT tokens via `get_current_user` / `get_current_active_user` dependencies
- **API:** RESTful with consistent `ApiResponse` envelope: `{success, message, data, pagination}`
- **CORS:** Configured via `CORS_ORIGINS` env var (comma-separated origins)
- **Env Vars:** All settings in `backend/app/core/config.py` with sensible defaults

## Coding Conventions
- Python: Black (88 chars), Ruff linting, MyPy type checking
- TypeScript: Explicit types, functional components, Tailwind CSS classes
- All API routes require auth via `get_current_active_user` unless public
- New features should follow the existing layered architecture pattern
