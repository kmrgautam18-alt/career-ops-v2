# 🖥️ RHEL 10.2 VM Deployment Guide

> **Deploy Career-Ops v2 on Red Hat Enterprise Linux 10.2**
> Complete step-by-step instructions — from bare OS to fully running production stack.

---

## 🚀 Quick Deploy (Interactive — 2 Minutes)

The **interactive deploy script** automates everything: Docker, DNS, HTTPS, AI keys, admin accounts, automation, and monitoring — all with smart defaults.

```bash
# One command — just run it and follow the prompts
# (Press Enter to accept defaults for any prompt)
bash scripts/deploy-rhel-interactive.sh

# Or download directly from GitHub (no clone needed):
curl -fsSL https://raw.githubusercontent.com/kmrgautam18-alt/career-ops-v2/main/scripts/deploy-rhel-interactive.sh | bash
```

### What the Interactive Script Does

| Phase | What Happens | Auto-Default? |
|-------|-------------|:-------------:|
| 1️⃣ Configuration | Prompts for DuckDNS, Gemini, Cloudflare, Telegram, SMTP, OAuth | ✅ All fields default |
| 2️⃣ System Setup | Auto-detects Podman (RHEL default) or Docker, installs needed engine + compose + git, curl, jq, openssl, cronie | ✅ Fully automated |
| 3️⃣ Clone & Clone | Clones repo, generates `.env` with random secrets | ✅ Fully automated |
| 4️⃣ DuckDNS | Sets up free `yourname.duckdns.org` domain with cron | ⏭️ Skips if no token |
| 5️⃣ Cloudflare | Creates free HTTPS tunnel | ⏭️ Skips if no token |
| 6️⃣ Telegram | Configures bot notifications | ⏭️ Skips if no token |
| 7️⃣ Container Stack | Builds & starts all 16 containers via detected engine | ✅ Fully automated |
| 8️⃣ DB & Admin | Runs migrations, creates admin user | ✅ Auto-created |
| 9️⃣ Automation | Sets up daily backups + LinkedIn + n8n | ✅ Fully automated |
| ✅ Verification | Health-checks backend, Prometheus, Grafana | ✅ Auto-verified |
| 🎉 Summary | Saves credentials to `~/.careerops-credentials` | ✅ Done |

```bash
# Preview what it will do without making any changes:
bash scripts/deploy-rhel-interactive.sh --dry-run
```

> **💡 Tip:** Run with `--dry-run` first to see exactly what the script will do. Then re-run without it to deploy for real.

---

## 📋 Manual Deployment (Step-by-Step)

> Use this guide if you prefer full control over each step, or if the interactive script doesn't fit your environment.

---

### Prerequisites

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| OS | RHEL 10.2 | RHEL 10.2 |
| RAM | 2 GB | 4 GB+ |
| CPU | 2 vCPUs | 4 vCPUs |
| Disk | 20 GB | 40 GB+ |
| Domain/IP | Public IP or domain | Domain with DNS |
| Network | Ports 80, 443, 3001, 9090 open | All ports behind firewall |

---

## 🧩 What You'll Deploy

| Service | Container | Port | Purpose |
|---------|-----------|------|---------|
| 🗄️ PostgreSQL | `careerops-db` | `:5432` | Production database |
| 🚀 Backend | `careerops-backend` | `:8000` | FastAPI + AI engine |
| 🌐 Frontend | `careerops-frontend` | `:80` | React SPA via Nginx |
| 📊 Prometheus | `careerops-prometheus` | `:9090` | Metrics collection |
| 📈 Grafana | `careerops-grafana` | `:3001` | Dashboards & alerts |
| 🔔 Alertmanager | `careerops-alertmanager` | `:9093` | Alert routing |
| 📝 Loki | `careerops-loki` | `:3100` | Log aggregation |
| 🔍 Promtail | `careerops-promtail` | — | Log collector |
| 🗃️ Postgres Exporter | `careerops-postgres-exporter` | `:9187` | DB metrics |
| 🌐 Nginx Exporter | `careerops-nginx-exporter` | `:9113` | Web server metrics |

**Total: 10 services** — all managed via Docker Compose.

---

## 🪜 Step 1 — Install Container Engine (Podman or Docker)

**Option A — Podman (RHEL native, auto-detected by script):**
```bash
# RHEL ships Podman by default. This is what the interactive script installs:
sudo dnf install -y podman podman-docker podman-compose
```

**Option B — Docker CE (alternative):**
```bash
sudo dnf config-manager --add-repo https://download.docker.com/linux/rhel/docker-ce.repo
sudo dnf install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
sudo systemctl enable --now docker
sudo usermod -aG docker $USER
```

---

## 🪜 Step 2 — Clone the Project

```bash
# 2.1 Install Git if not already installed
sudo dnf install -y git

# 2.2 Clone the repository
cd ~
git clone https://github.com/kmrgautam18-alt/career-ops-v2.git
cd career-ops-v2

# 2.3 Verify you have all required files
ls -la
# Should see: Dockerfile, docker-compose.yml, .env.example, backend/, frontend/, monitoring/
```

---

## 🪜 Step 3 — Configure Environment Variables

```bash
# 3.1 Create .env from template
cp .env.example .env

# 3.2 Generate a secure secret key
openssl rand -hex 32
# Copy the output — you'll paste it below

# 3.3 Generate a PostgreSQL password
openssl rand -base64 24
# Copy the output

# 3.4 Edit the .env file
nano .env
```

### Required Variables — Paste These Values

```ini
# ── Database ──────────────────────────────────
POSTGRES_USER=careerops
POSTGRES_PASSWORD=<paste-the-base64-password-here>
POSTGRES_DB=careerops

# ── Backend ──────────────────────────────────
SECRET_KEY=<paste-the-hex-secret-here>
CORS_ORIGINS=http://your-vm-ip,http://your-domain.com
APP_ENV=production
DEBUG=false

# ── AI / LLM (optional — get free key) ───────
# Get a free Gemini API key at https://aistudio.google.com/apikey
LLM_API_KEY=<your-gemini-api-key>
LLM_MODEL=gemini-2.0-flash
LLM_PROVIDER=google

# ── Monitoring ───────────────────────────────
GRAFANA_ADMIN_USER=admin
GRAFANA_ADMIN_PASSWORD=<choose-a-strong-password>
```

<details>
<summary>📌 Click here for a complete .env example</summary>

```ini
# Application
APP_NAME=Career-Ops
APP_VERSION=0.1.0
APP_ENV=production
DEBUG=false

# Database
DATABASE_URL=postgresql://careerops:YOUR_PASSWORD@postgres:5432/careerops
POSTGRES_USER=careerops
POSTGRES_PASSWORD=YOUR_POSTGRES_PASSWORD
POSTGRES_DB=careerops
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20

# CORS
CORS_ORIGINS=http://localhost:3000,http://your-domain.com
CORS_ALLOW_CREDENTIALS=true

# JWT
SECRET_KEY=YOUR_GENERATED_64_CHAR_HEX
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# LLM
LLM_API_KEY=YOUR_GEMINI_KEY
LLM_MODEL=gemini-2.0-flash
LLM_PROVIDER=google

# Baserow (optional)
BASEROW_URL=https://api.baserow.io
BASEROW_TOKEN=

# Grafana
GRAFANA_ADMIN_USER=admin
GRAFANA_ADMIN_PASSWORD=YOUR_GRAFANA_PASSWORD
```
</details>

---

## 🪜 Step 4 — Configure Firewall

```bash
# 4.1 Open required ports
sudo firewall-cmd --permanent --add-service=http    # Port 80 — Frontend
sudo firewall-cmd --permanent --add-service=https   # Port 443 — HTTPS (future)
sudo firewall-cmd --permanent --add-port=3001/tcp   # Port 3001 — Grafana
sudo firewall-cmd --permanent --add-port=9090/tcp   # Port 9090 — Prometheus
sudo firewall-cmd --permanent --add-port=9093/tcp   # Port 9093 — Alertmanager

# 4.2 Reload firewall
sudo firewall-cmd --reload

# 4.3 Verify rules
sudo firewall-cmd --list-all
```

---

## 🪜 Step 5 — Build & Start the Stack

```bash
# 5.1 Build images and start all containers
docker compose up -d --build

# 5.2 Wait for everything to initialize (give it 30 seconds)
sleep 30

# 5.3 Check all services are running
docker compose ps

# Expected output — all 10 services should show "Up" or "Healthy":
# ✔ careerops-db                 Up (healthy)
# ✔ careerops-backend            Up
# ✔ careerops-frontend           Up
# ✔ careerops-prometheus         Up
# ✔ careerops-grafana            Up
# ✔ careerops-alertmanager       Up
# ✔ careerops-loki               Up
# ✔ careerops-promtail           Up
# ✔ careerops-postgres-exporter  Up
# ✔ careerops-nginx-exporter     Up
```

---

## 🪜 Step 6 — Run Database Migrations

```bash
# 6.1 Apply Alembic migrations
docker compose exec backend alembic upgrade head

# Expected output:
# INFO  [alembic.runtime.migration] Running upgrade  -> fb3db3a182e7, initial_schema

# 6.2 (Alternative) If Alembic isn't set up, initialize directly:
docker compose exec backend python -c "
from backend.app.database.init_db import init_database;
init_database();
print('✅ Database initialized')
"
```

---

## 🪜 Step 7 — Verify Everything Works

### 7.1 Health Checks

Run each command and confirm you get a successful response:

```bash
# Backend API
curl http://localhost:8000/
# → {"application":"Career-Ops v2","status":"healthy"}

# Swagger Docs
curl -o /dev/null -s -w "HTTP %{http_code}\n" http://localhost:8000/docs
# → HTTP 200

# Prometheus
curl http://localhost:9090/-/ready
# → Prometheus is Ready

# Grafana
curl http://localhost:3001/api/health
# → {"database":"ok",...}

# Loki
curl http://localhost:3100/ready
# → ready

# Metrics endpoint
curl -s http://localhost:8000/metrics | head -5
# → # HELP careerops_http_requests_total ...
```

### 7.2 Test User Registration & Login

```bash
# Register a test user
curl -X POST http://localhost:8000/api/v1/users/register \
  -H 'Content-Type: application/json' \
  -d '{
    "email":"demo@careerops.io",
    "password":"Demo@123",
    "username":"demo_user",
    "full_name":"Demo User"
  }'

# Login to get JWT token
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"email":"demo@careerops.io","password":"Demo@123"}'

# Use the returned access_token in further requests
```

### 7.3 Test AI Features (if you set LLM_API_KEY)

```bash
# ATS Score (with dummy data — will use rule-based fallback if no API key)
curl -X POST http://localhost:8000/api/v1/ai/ats-score \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer YOUR_TOKEN' \
  -d '{
    "resume_text": "Python developer with 5 years experience in Docker and Kubernetes",
    "job_description": "Looking for a Python developer with Docker and Kubernetes experience"
  }'
```

---

## 🪜 Step 8 — Access the Services

| Service | URL | Notes |
|---------|-----|-------|
| 🌐 **Frontend** | `http://your-vm-ip/` | Main application UI |
| 📖 **API Docs** | `http://your-vm-ip/api/docs` | Interactive Swagger UI |
| 📊 **Prometheus** | `http://your-vm-ip:9090` | Metrics explorer |
| 📈 **Grafana** | `http://your-vm-ip:3001` | Dashboards (`admin` / password from .env) |
| 🔔 **Alertmanager** | `http://your-vm-ip:9093` | Alert status UI |
| 📝 **Loki** | `http://your-vm-ip:3100/ready` | Log system health |

---

## 🪜 Step 9 — Set Up Slack Alerts (Optional)

```bash
# 9.1 Edit the Alertmanager config
nano monitoring/alertmanager/alertmanager.yml
```

Find this section and uncomment + replace with your Slack webhook URL:

```yaml
global:
  slack_api_url: 'https://hooks.slack.com/services/YOUR/TEAM/TOKEN-HERE'
```

```bash
# 9.2 Restart Alertmanager to apply changes
docker compose restart alertmanager
```

---

## 🪜 Step 10 — Restart & Update

```bash
# View logs for any service
docker compose logs -f backend          # Backend logs (live tail)
docker compose logs -f grafana          # Grafana logs
docker compose logs --tail=100 backend  # Last 100 lines

# Restart a single service
docker compose restart backend

# Update the stack after pulling new code
git pull origin main
docker compose up -d --build
docker compose exec backend alembic upgrade head

# Stop everything
docker compose down

# Full reset (⚠️ deletes all data including database)
docker compose down -v
```

---

## 🪜 Step 11 — Set Up HTTPS (Optional but Recommended)

```bash
# 11.1 Install Certbot
sudo dnf install -y certbot python3-certbot-nginx

# 11.2 Obtain SSL certificate
sudo certbot --nginx -d your-domain.com

# 11.3 Certbot auto-renews — verify
sudo certbot renew --dry-run
```

---

## 🧪 Troubleshooting

### ❌ Docker permission denied

```bash
# Add user to docker group and restart session
sudo usermod -aG docker $USER
exec su -l $USER
```

### ❌ Container won't start

```bash
# Check detailed logs
docker compose logs <service-name>
# Example: docker compose logs backend

# Check if ports are already in use
sudo ss -tulpn | grep -E '80|8000|3001|9090|9093|3100'
```

### ❌ Database connection error

```bash
# Verify PostgreSQL is healthy
docker compose exec postgres pg_isready -U careerops

# Check the database URL in .env matches the docker compose config
# It should be: postgresql://careerops:YOUR_PASSWORD@postgres:5432/careerops
```

### ❌ Prometheus can't scrape targets

```bash
# Check Prometheus targets UI at http://your-vm-ip:9090/targets
# All targets should show "UP" status
```

### ❌ Grafana can't find Prometheus

```bash
# Verify datasource config
docker compose exec grafana cat /etc/grafana/provisioning/datasources/datasource.yml
# Should show url: http://prometheus:9090
```

---

## 🔍 Quick Reference: Useful Docker Commands

| Action | Command |
|--------|---------|
| Start all services | `docker compose up -d` |
| Stop all services | `docker compose down` |
| View all logs | `docker compose logs -f` |
| View backend logs | `docker compose logs -f backend` |
| Rebuild & restart | `docker compose up -d --build` |
| Restart single service | `docker compose restart backend` |
| Check container health | `docker compose ps` |
| Execute command in container | `docker compose exec backend bash` |
| Clean everything (loses data) | `docker compose down -v` |

---

## ✅ Deployment Checklist

- [ ] Docker installed and running
- [ ] Git clone completed
- [ ] `.env` file configured with secure passwords
- [ ] Firewall ports opened
- [ ] `docker compose up -d --build` completed
- [ ] Database migrations applied
- [ ] Health checks pass (backend, Prometheus, Grafana, Loki)
- [ ] Frontend accessible in browser
- [ ] HTTPS configured (if using a domain)
- [ ] Slack/email alerts configured (optional)

---

## 📞 Need Help?

- 📖 **Full Documentation:** [docs/](docs/) directory
- 🐛 **Issues:** [GitHub Issues](https://github.com/kmrgautam18-alt/career-ops-v2/issues)
- 📧 **Author:** Kumar Gautam — [GitHub](https://github.com/kmrgautam18-alt)
