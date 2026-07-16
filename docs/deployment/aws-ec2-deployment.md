# ☁️ AWS EC2 Deployment Guide

> **Deploy Career-Ops v2 on AWS EC2**
> Complete step-by-step instructions — from creating an EC2 instance to fully running production stack.

---

## 📋 Overview

This guide walks you through deploying Career-Ops v2 on **AWS EC2** running **Ubuntu 24.04 LTS**. The entire stack runs in Docker containers orchestrated by Docker Compose.

### Architecture on EC2

```
Internet ──▶ EC2 Instance (t3.medium)
                │
          ┌─────▼──────┐
          │  Nginx :80  │  ← Reverse proxy (serves frontend + proxies API)
          └─────┬──────┘
                │
          ┌─────▼──────┐
          │  Backend    │  ← FastAPI (port 8000)
          │  + AI       │
          └─────┬──────┘
                │
          ┌─────▼──────┐
          │ PostgreSQL  │  ← Production database
          └────────────┘
```

### Monitoring Architecture

```
          ┌──────────────┐
          │   Grafana    │  ← Dashboards + Alerts
          └──────┬───────┘
          ┌──────▼───────┐
          │  Prometheus  │  ← Metrics collection
          └──┬───┬───┬───┘
             │   │   │
        ┌────┘   │   └────┐
        ▼        ▼        ▼
    ┌────────┐ ┌────┐ ┌───────┐
    │Backend │ │DB  │ │ Nginx │
    │Metrics │ │    │ │Status │
    └────────┘ └────┘ └───────┘
```

---

## 🪜 Step 1 — Launch an EC2 Instance

1. Go to the **[AWS EC2 Console](https://console.aws.amazon.com/ec2/)**
2. Click **Launch Instance**

### Configuration

| Setting | Value |
|---------|-------|
| **Name** | `career-ops-prod` |
| **AMI** | **Ubuntu 24.04 LTS** (HVM, SSD Volume Type) |
| **Instance Type** | `t3.medium` (2 vCPU, 4 GB RAM) — Good starting point |
| **Key Pair** | Create new or select existing `.pem` key — **save it securely!** |
| **VPC** | Default VPC |
| **Subnet** | Default subnet (any availability zone) |
| **Auto-assign Public IP** | **Enable** |
| **Storage** | 20 GB gp3 — Increase to 30 GB if enabling monitoring |
| **Security Group** | Create new (see below) |

### Security Group Rules

| Type | Protocol | Port | Source | Purpose |
|------|----------|------|--------|---------|
| SSH | TCP | 22 | `0.0.0.0/0` | Admin access (⛔ restrict to your IP in production) |
| HTTP | TCP | 80 | `0.0.0.0/0` | Frontend + API (via Nginx) |
| HTTPS | TCP | 443 | `0.0.0.0/0` | TLS termination (add later) |
| Custom TCP | TCP | 3001 | `0.0.0.0/0` | Grafana (⛔ restrict in production) |
| Custom TCP | TCP | 9090 | `0.0.0.0/0` | Prometheus (⛔ restrict in production) |

> ⚠️ **DO NOT open port 8000 to the public!** The Nginx reverse proxy handles API requests internally.

3. Click **Launch Instance**
4. Wait for the instance state to show **Running**

---

## 🪜 Step 2 — Connect to Your EC2 Instance

```bash
# 2.1 Set proper permissions on your key file
chmod 400 /path/to/your-key.pem

# 2.2 SSH into the instance
ssh -i /path/to/your-key.pem ubuntu@ec2-xx-xx-xx-xx.compute-1.amazonaws.com

# Replace ec2-xx-xx-xx-xx with your instance's public DNS
# You can find this in the EC2 console under "Public IPv4 DNS"
```

---

## 🪜 Step 3 — Install Docker & Docker Compose

Run these commands **inside the EC2 instance**:

```bash
# 3.1 Update system packages
sudo apt update && sudo apt upgrade -y

# 3.2 Install Docker dependencies
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common

# 3.3 Add Docker's official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# 3.4 Add Docker repository
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 3.5 Install Docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# 3.6 Start and enable Docker
sudo systemctl enable --now docker

# 3.7 Add ubuntu user to docker group
sudo usermod -aG docker ubuntu

# 3.8 Apply group changes (log out and back in, or run:)
newgrp docker

# 3.9 Verify installation
docker --version
docker compose version
```

---

## 🪜 Step 4 — Clone the Project

```bash
# 4.1 Clone the repository
cd ~
git clone https://github.com/kmrgautam18-alt/career-ops-v2.git
cd career-ops-v2

# 4.2 Verify project structure
ls -la
# Should see: Dockerfile, docker-compose.yml, .env.example, backend/, frontend/, monitoring/
```

---

## 🪜 Step 5 — Configure Environment

```bash
# 5.1 Create .env from template
cp .env.example .env

# 5.2 Generate secure secrets
openssl rand -hex 32    # → SECRET_KEY
openssl rand -base64 24 # → POSTGRES_PASSWORD

# 5.3 Edit the .env file
nano .env
```

### Set These Values

```ini
# ── Database ──────────────────────────────────
POSTGRES_USER=careerops
POSTGRES_PASSWORD=<paste-base64-password>
POSTGRES_DB=careerops

# ── Backend ──────────────────────────────────
SECRET_KEY=<paste-hex-secret>
CORS_ORIGINS=http://ec2-xx-xx-xx-xx.compute-1.amazonaws.com
APP_ENV=production
DEBUG=false

# ── AI / LLM (optional) ──────────────────────
# Get free key: https://aistudio.google.com/apikey
LLM_API_KEY=<your-gemini-key>
LLM_MODEL=gemini-2.0-flash
LLM_PROVIDER=google

# ── Monitoring ───────────────────────────────
GRAFANA_ADMIN_USER=admin
GRAFANA_ADMIN_PASSWORD=<choose-strong-password>
```

---

## 🪜 Step 6 — Build & Start the Stack

```bash
# 6.1 Build all images and start services
docker compose up -d --build

# 6.2 Wait for database to be healthy (give it 30 seconds)
sleep 30

# 6.3 Verify all containers are running
docker compose ps

# Expected: All 10 services showing "Up" or "Healthy"
```

---

## 🪜 Step 7 — Run Database Migrations

```bash
# 7.1 Apply migrations
docker compose exec backend alembic upgrade head

# 7.2 Alternative (if no Alembic): initialize directly
docker compose exec backend python -c "
from backend.app.database.init_db import init_database;
init_database();
print('✅ Database initialized successfully');
"
```

---

## 🪜 Step 8 — Verify the Deployment

### 8.1 Health Checks

```bash
# Backend health
curl http://localhost:8000/
# → {"application":"Career-Ops v2","status":"healthy"}

# Frontend (via Nginx)
curl -o /dev/null -s -w "HTTP %{http_code}\n" http://localhost/
# → HTTP 200

# API proxy (through Nginx)
curl http://localhost/api/v1/
# → API response

# Prometheus
curl -o /dev/null -s -w "HTTP %{http_code}\n" http://localhost:9090/-/ready
# → HTTP 200

# Grafana
curl -o /dev/null -s -w "HTTP %{http_code}\n" http://localhost:3001/api/health
# → HTTP 200

# Prometheus metrics
curl -s http://localhost:8000/metrics | head -10
# → # HELP careerops_http_requests_total ...
```

### 8.2 Test Full Flow

```bash
# Register a user
curl -X POST http://localhost/api/v1/users/register \
  -H 'Content-Type: application/json' \
  -d '{
    "email":"admin@careerops.io",
    "password":"Secure@123",
    "username":"admin",
    "full_name":"Admin User"
  }'

# Login
TOKEN=$(curl -s -X POST http://localhost/api/v1/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"email":"admin@careerops.io","password":"Secure@123"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['access_token'])")

echo "Token: $TOKEN"

# Test authenticated endpoint
curl -s http://localhost/api/v1/users/me \
  -H "Authorization: Bearer $TOKEN"
```

---

## 🪜 Step 9 — Set Up HTTPS (Free with Let's Encrypt)

Prerequisite: You need a **domain name** pointing to your EC2 instance's public IP.

```bash
# 9.1 Install Nginx (for Certbot standalone mode)
sudo apt install -y nginx certbot python3-certbot-nginx

# 9.2 Obtain certificate
sudo certbot --nginx -d your-domain.com \
  --non-interactive --agree-tos -m your-email@example.com

# 9.3 Verify auto-renewal
sudo certbot renew --dry-run

# 9.4 Restart the frontend container to pick up HTTPS
docker compose restart frontend

# Update CORS_ORIGINS in .env to include https://
nano .env
# Change: CORS_ORIGINS=https://your-domain.com
docker compose restart backend
```

> 📘 **No domain?** You can still use the stack over HTTP on the public IP. Skip this step.

---

## 🪜 Step 10 — Enable Slack/PagerDuty Alerts (Optional)

### Slack Webhook

1. Go to your Slack workspace: **Apps** → **Incoming Webhooks** → **Add Configuration**
2. Choose a channel and copy the webhook URL
3. Edit the Alertmanager config:

```bash
nano monitoring/alertmanager/alertmanager.yml
```

Uncomment and set:

```yaml
global:
  slack_api_url: 'https://hooks.slack.com/services/YOUR/TEAM/TOKEN-HERE'
```

```bash
# Restart Alertmanager
docker compose restart alertmanager
```

---

## 🪜 Step 11 — Access Your Deployed Application

| Service | URL | Credentials |
|---------|-----|-------------|
| 🌐 **Frontend** | `http://ec2-xx-xx-xx-xx.compute-1.amazonaws.com/` | — |
| 📖 **API Docs** | `http://ec2-xx-xx-xx-xx.compute-1.amazonaws.com/api/docs` | — |
| 📊 **Prometheus** | `http://ec2-xx-xx-xx-xx.compute-1.amazonaws.com:9090` | — |
| 📈 **Grafana** | `http://ec2-xx-xx-xx-xx.compute-1.amazonaws.com:3001` | `admin` / your password |
| 🔔 **Alertmanager** | `http://ec2-xx-xx-xx-xx.compute-1.amazonaws.com:9093` | — |

---

## 🪜 Step 12 — Maintenance & Updates

### Daily Operations

```bash
# View logs
docker compose logs -f backend          # Live tail backend logs
docker compose logs --tail=100 backend  # Last 100 lines
docker compose logs -f grafana          # Grafana logs

# Restart a service
docker compose restart backend

# Check service health
docker compose ps
```

### Update the Stack After Code Changes

```bash
# From the EC2 instance
cd ~/career-ops-v2
git pull origin main
docker compose up -d --build
docker compose exec backend alembic upgrade head
```

### Monitor Your Monitoring

```bash
# Check disk usage
df -h

# Check Docker disk usage
docker system df

# Clean up unused images (safe to run)
docker image prune -f

# Full system cleanup (removes unused containers, networks, images)
docker system prune -f
```

### Create Backups

```bash
# Backup PostgreSQL database
docker compose exec -T postgres pg_dump -U careerops careerops > ~/backup-$(date +%Y%m%d).sql

# Restore from backup
cat ~/backup-20260716.sql | docker compose exec -T postgres psql -U careerops careerops
```

---

## 💰 Cost Estimation

| Resource | t3.medium (2 vCPU, 4 GB) | t3.large (2 vCPU, 8 GB) |
|----------|--------------------------|--------------------------|
| EC2 (on-demand, us-east-1) | ~$30/month | ~$60/month |
| EBS 20 GB gp3 | ~$2/month | ~$2/month |
| **Total (approx)** | **~$32/month** | **~$62/month** |

> 💡 **Save 60%+** by using **Reserved Instances** or **Spot Instances**.

---

## 🧪 Troubleshooting

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| `curl: Connection refused` | Service not started | `docker compose ps` to check status |
| `docker: permission denied` | User not in docker group | `sudo usermod -aG docker $USER && newgrp docker` |
| Database connection error | .env credentials mismatch | Check `POSTGRES_PASSWORD` matches in .env |
| 502 Bad Gateway | Backend not ready | `docker compose logs backend` for errors |
| Prometheus targets DOWN | Service unreachable | Check `docker compose ps` for target service |
| Frontend shows blank page | Build error | `docker compose logs frontend` |
| Port already in use | Another process occupying port | `sudo lsof -i :80` then `sudo systemctl stop nginx` |

---

## ✅ Deployment Checklist

- [ ] EC2 instance launched with correct security group
- [ ] SSH key saved with `chmod 400`
- [ ] Docker installed and running
- [ ] Git clone completed
- [ ] `.env` configured with strong secrets
- [ ] `docker compose up -d --build` completed
- [ ] Database migrations applied
- [ ] All 10 health checks pass
- [ ] User registration + login works
- [ ] AI features work (if API key set)
- [ ] Frontend accessible from browser
- [ ] HTTPS configured (if domain available)
- [ ] Slack/PagerDuty alerts configured (optional)
- [ ] Backup plan in place

---

## 📚 Related Resources

| Resource | Link |
|----------|------|
| 📖 RHEL Deployment Guide | [`rhel-vm-deployment.md`](rhel-vm-deployment.md) |
| 🏗️ Architecture Docs | [`docs/architecture/`](../architecture/) |
| 📊 Monitoring Setup | [`monitoring/`](../../monitoring/) |
| 🐳 Docker Compose Config | [`docker-compose.yml`](../../docker-compose.yml) |
| 🔧 Environment Template | [`.env.example`](../../.env.example) |
| 📝 Project README | [`README.md`](../../README.md) |

---

## 📞 Need Help?

- 📖 **Full Documentation:** [docs/](../) directory
- 🐛 **Issues:** [GitHub Issues](https://github.com/kmrgautam18-alt/career-ops-v2/issues)
- 📧 **Author:** Kumar Gautam — [GitHub](https://github.com/kmrgautam18-alt)
