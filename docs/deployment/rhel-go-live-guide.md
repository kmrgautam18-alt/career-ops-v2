# 🌐 Career-Ops Go-Live Guide — RHEL 10.2

> **Make Career-Ops v2 Live on the Internet**
> From a fresh RHEL 10.2 VM to a fully running, publicly accessible production platform with domain, HTTPS, AI, monitoring, and real-time results.

---

## 📋 What We're Building

```
                    ┌──────────────────┐
                    │   Your Domain    │
                    │ careerops.com    │
                    └────────┬─────────┘
                             │ DNS → VM IP
                             ▼
              ┌──────────────────────────┐
              │   🌐 Nginx (port 80/443) │
              │   HTTPS with Let's Encrypt│
              │   SPA + API proxy        │
              └────────┬─────────────────┘
                       │
          ┌────────────┼────────────┬──────────────┐
          ▼            ▼            ▼              ▼
    ┌──────────┐ ┌──────────┐ ┌────────┐ ┌──────────────┐
    │  React   │ │ FastAPI  │ │Postgres│ │  Monitoring  │
    │ Frontend │ │ Backend  │ │   DB   │ │ Prom+Grafana │
    └──────────┘ └──────────┘ └────────┘ └──────────────┘
```

---

## 📌 Prerequisites

| Requirement | Details |
|-------------|---------|
| **RHEL 10.2 VM** | Any provider (on-prem, Vultr, Linode, Hetzner, DigitalOcean) |
| **Public IP** | Static public IP address |
| **Domain Name** | e.g. `careerops.com` or `careerops.yourname.com` |
| **RAM** | 4 GB minimum, 8 GB recommended |
| **Disk** | 30 GB minimum |
| **Ports** | 22 (SSH), 80 (HTTP), 443 (HTTPS) must be open |

---

## 🪜 Phase 1: Server Setup

### Step 1.1 — Start Your VM

Provision a RHEL 10.2 VM from your provider and note the **public IP**.

### Step 1.2 — SSH In

```bash
ssh root@your-vm-ip
# Or if using a non-root user:
ssh username@your-vm-ip
```

### Step 1.3 — Update System

```bash
# Update all packages
sudo dnf update -y

# Install essential tools
sudo dnf install -y git curl wget nano firewalld

# Enable firewall
sudo systemctl enable --now firewalld
```

### Step 1.4 — Install Docker & Docker Compose

```bash
# Add Docker repository
sudo dnf config-manager --add-repo https://download.docker.com/linux/rhel/docker-ce.repo

# Install Docker
sudo dnf install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Start and enable Docker
sudo systemctl enable --now docker

# Add your user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Verify
docker --version && docker compose version
```

---

## 🪜 Phase 2: Domain & DNS

### Step 2.1 — Point Your Domain to Your VM

Go to your domain registrar's DNS settings and create an **A record**:

| Type | Name | Value |
|------|------|-------|
| **A** | `@` (or `careerops.com`) | `YOUR_VM_PUBLIC_IP` |
| **A** | `www` | `YOUR_VM_PUBLIC_IP` |

### Step 2.2 — Verify DNS Propagation

```bash
# From your local machine
ping your-domain.com
# Should show your VM's public IP

dig +short your-domain.com
# Should return: YOUR_VM_PUBLIC_IP
```

> ⏳ DNS changes can take **5 minutes to 24 hours** to propagate.

---

## 🪜 Phase 3: Deploy the Stack

### Step 3.1 — Clone the Repository

```bash
cd ~
git clone https://github.com/kmrgautam18-alt/career-ops-v2.git
cd career-ops-v2
```

### Step 3.2 — Create .env File

```bash
cp .env.example .env
```

### Step 3.3 — Generate Secure Secrets

```bash
# JWT Secret Key (for token signing)
SECRET_KEY=$(openssl rand -hex 32)
echo "SECRET_KEY=$SECRET_KEY" >> .env

# PostgreSQL Password
POSTGRES_PASSWORD=$(openssl rand -base64 24)
echo "POSTGRES_PASSWORD=$POSTGRES_PASSWORD" >> .env

# Grafana Admin Password
GRAFANA_PASSWORD=$(openssl rand -base64 16)
echo "GRAFANA_ADMIN_PASSWORD=$GRAFANA_PASSWORD" >> .env

# n8n Encryption Key
N8N_KEY=$(openssl rand -hex 32)
echo "N8N_ENCRYPTION_KEY=$N8N_KEY" >> .env
```

### Step 3.4 — Set Domain-Specific Variables

```bash
# Edit .env
nano .env
```

Update these values in `.env`:

```ini
# Replace with your actual domain
CORS_ORIGINS=https://your-domain.com,https://www.your-domain.com

# n8n webhook URL (for receiving backend events)
N8N_HOST=your-domain.com
N8N_WEBHOOK_BASE_URL=http://n8n:5678
N8N_ENABLED=false                    # Set to true after activating n8n workflows
```

### Step 3.5 — Set the Gemini API Key

```bash
# Enter your Gemini API key (get free at https://aistudio.google.com/apikey)
nano .env
# Add: LLM_API_KEY=your-actual-gemini-key-here
```

### Step 3.6 — Configure Firewall

```bash
# Open only the ports the internet needs to access
sudo firewall-cmd --permanent --add-service=http    # Port 80
sudo firewall-cmd --permanent --add-service=https   # Port 443
sudo firewall-cmd --reload

# All other ports (8000, 3001, 9090, etc.) stay closed for security
# They're only accessible inside the Docker network
```

### Step 3.7 — Build & Start All Services

```bash
# Build all Docker images and start the stack
docker compose up -d --build

# Wait for PostgreSQL to be healthy
sleep 15

# Verify all services are running
docker compose ps

# Expected output (you'll see all 13 services in "Up" status):
# careerops-db, careerops-backend, careerops-frontend,
# careerops-prometheus, careerops-grafana, careerops-alertmanager,
# careerops-loki, careerops-promtail, careerops-postgres-exporter,
# careerops-nginx-exporter, careerops-n8n
```

### Step 3.8 — Run Database Migrations

```bash
docker compose exec backend alembic upgrade head
```

---

## 🪜 Phase 4: Verify Locally

### Step 4.1 — Backend Health Check

```bash
curl http://localhost:8000/
# Expected: {"application":"Career-Ops v2","status":"healthy"}
```

### Step 4.2 — Frontend via Nginx

```bash
curl -s -o /dev/null -w "HTTP %{http_code}" http://localhost/
# Expected: HTTP 200
```

### Step 4.3 — API Through Nginx Proxy

```bash
curl http://localhost/api/v1/
# Should return API response
```

### Step 4.4 — Prometheus Metrics

```bash
curl -s http://localhost:8000/metrics | head -10
# Expected: # HELP careerops_http_requests_total ...
```

### Step 4.5 — Test AI Features

```bash
# Register a test user
curl -X POST http://localhost/api/v1/users/register \
  -H 'Content-Type: application/json' \
  -d '{"email":"admin@mydomain.com","password":"Admin@123","username":"admin","full_name":"Admin"}'

# Login
TOKEN=$(curl -s -X POST http://localhost/api/v1/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"email":"admin@mydomain.com","password":"Admin@123"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['access_token'])")

# Test ATS Scoring with real Gemini AI
curl -X POST http://localhost/api/v1/ai/ats-score \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "resume_text": "Python developer with 5 years Docker and AWS experience",
    "job_description": "Senior backend engineer with Python, Docker, and cloud"
  }'

# Expected: Real AI score with strengths, weaknesses, and recommendations!
```

---

## 🪜 Phase 5: Set Up HTTPS (Critical for Go-Live)

### Step 5.1 — Install Certbot

```bash
sudo dnf install -y certbot python3-certbot-nginx
```

### Step 5.2 — Stop Frontend Nginx Temporarily

```bash
docker compose stop frontend
```

### Step 5.3 — Get SSL Certificate

```bash
sudo certbot certonly --standalone -d your-domain.com -d www.your-domain.com \
  --non-interactive --agree-tos -m admin@your-domain.com

# Files created at:
# /etc/letsencrypt/live/your-domain.com/fullchain.pem
# /etc/letsencrypt/live/your-domain.com/privkey.pem
```

### Step 5.4 — Create SSL-Enabled Frontend Config

```bash
# Create an SSL nginx config
cat > frontend/nginx-ssl.conf << 'NGINXSSL'
# ==========================================
# Career-Ops Frontend — Nginx SSL Config
# ==========================================

server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com www.your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;

    root /usr/share/nginx/html;
    index index.html;

    # API proxy
    location /api/ {
        proxy_pass http://backend:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 120s;
        proxy_send_timeout 120s;
    }

    # SPA fallback
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Static assets
    location /assets/ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
NGINXSSL

# Restart frontend
docker compose up -d --build frontend
```

### Step 5.5 — Update CORS for HTTPS

```bash
nano .env
# Change to:
# CORS_ORIGINS=https://your-domain.com,https://www.your-domain.com
docker compose restart backend
```

### Step 5.6 — Set Up Auto-Renewal

```bash
# Certbot creates a systemd timer automatically
sudo systemctl status certbot-renew.timer

# Test renewal
sudo certbot renew --dry-run
```

---

## 🪜 Phase 6: Final Verification — Public Access

### Step 6.1 — Test from Any Browser

Open **https://your-domain.com** in any browser:

| What to Test | Expected Result |
|-------------|----------------|
| Landing page loads | ✅ Beautiful dark-themed landing page |
| SSL / HTTPS | ✅ Green padlock in browser |
| Register new account | ✅ User created successfully |
| Login | ✅ JWT token returned |
| Dashboard | ✅ Stats load with real data |
| Jobs page | ✅ Create, search, filter jobs |
| Applications | ✅ CRUD with status tracking |
| Resumes | ✅ Upload and download files |
| AI Tools | ✅ Real AI results from Gemini (ATS, interviews, optimization) |

### Step 6.2 — Test API Endpoints

```bash
# From your local machine
curl https://your-domain.com/api/v1/
# Should return API response

curl https://your-domain.com/
# Should return the React app HTML

# Register via public API
curl -X POST https://your-domain.com/api/v1/users/register \
  -H 'Content-Type: application/json' \
  -d '{"email":"newuser@example.com","password":"NewUser@123","username":"newuser","full_name":"New User"}'
```

### Step 6.3 — Test Monitoring & Logging

```bash
# Check Prometheus (internally)
curl http://localhost:9090/targets

# Check Grafana
curl http://localhost:3001/api/health

# View backend logs (real-time)
docker compose logs --tail=50 backend
```

---

## 🪜 Phase 7: Enable n8n Workflows (Optional)

```bash
# Visit https://your-domain.com:5678 in your browser
# Create an admin account
# Import workflows from monitoring/n8n/workflows/

# Then enable webhooks:
nano .env
# Set: N8N_ENABLED=true
docker compose restart backend
```

---

## 🪜 Phase 8: Enable Slack Alerts (Optional)

```bash
nano monitoring/alertmanager/alertmanager.yml
# Uncomment: slack_api_url: 'https://hooks.slack.com/services/...'
docker compose restart alertmanager
```

---

## 🪜 Phase 9: Maintenance

### Daily Operations

```bash
# View live logs
docker compose logs -f backend

# Restart a service
docker compose restart backend

# Check disk usage
df -h
```

### Update the Application

```bash
git pull origin main
docker compose up -d --build
docker compose exec backend alembic upgrade head
```

### Backup the Database

```bash
docker compose exec -T postgres pg_dump -U careerops careerops > ~/backup-$(date +%Y%m%d-%H%M).sql
```

### Monitor Disk Space

```bash
# Check Docker disk usage
docker system df

# Clean up old images
docker image prune -af

# Clean up everything unused
docker system prune -af
```

---

## 🧪 Troubleshooting Guide

### 🔴 Website Not Loading

| Symptom | Check | Fix |
|---------|-------|-----|
| DNS not resolving | `dig your-domain.com` | Update A record at registrar |
| Nginx not responding | `curl http://localhost/` | `docker compose ps` check frontend |
| HTTP works, HTTPS doesn't | Check certbot status | Re-run `sudo certbot --nginx` |
| 502 Bad Gateway | `docker compose logs backend` | Backend not running |

### 🔴 Docker Issues

```bash
# Container won't start
docker compose logs <service-name>

# Port conflict
sudo lsof -i :80

# Permission denied
sudo usermod -aG docker $USER && newgrp docker
```

### 🔴 Database Issues

```bash
# Check PostgreSQL health
docker compose exec postgres pg_isready -U careerops

# Re-run migrations
docker compose exec backend alembic upgrade head

# Reset database (⚠️ deletes data)
docker compose down -v && docker compose up -d --build
```

### 🔴 AI Not Working

```bash
# Check if API key is set
grep LLM_API_KEY .env

# Test with curl
curl http://localhost:8000/api/v1/ai/ats-score \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"resume_text":"test","job_description":"test"}'

# Check backend logs
docker compose logs backend | grep -i "llm\|gemini\|ai"
```

---

## ✅ Go-Live Checklist

- [ ] VM provisioned with RHEL 10.2
- [ ] Docker installed and running
- [ ] Domain DNS A record points to VM IP
- [ ] Git clone completed
- [ ] `.env` configured with all secrets
- [ ] Gemini API key set (AI will work)
- [ ] Firewall configured (ports 80, 443 only)
- [ ] `docker compose up -d --build` succeeded
- [ ] Database migrations applied
- [ ] HTTPS configured with Let's Encrypt
- [ ] All health checks pass
- [ ] User registration + login works from browser
- [ ] AI features return real results
- [ ] Grafana dashboards accessible
- [ ] Monitoring metrics flowing
- [ ] Backups scheduled
- [ ] SSL auto-renewal verified

---

## 📊 Real-Time Results — What Users Will See

| Feature | Real-Time Result |
|---------|-----------------|
| 🔐 **Login/Register** | Instant JWT authentication |
| 💼 **Job Management** | Create, search, filter in real-time |
| 📋 **Application Tracking** | Status changes update immediately |
| 📄 **Resume Upload** | Drag-and-drop with progress bar |
| 🤖 **ATS Score** | Live score with strengths, weaknesses, recommendations |
| 📊 **Dashboard** | Real-time stats on jobs, applications, interviews |
| 📈 **Grafana Monitoring** | Live metrics on requests, errors, latency |
| 📝 **Loki Logs** | Queryable logs for all services |

---

## 📞 Getting Help

- 📖 **Full Docs:** [github.com/kmrgautam18-alt/career-ops-v2/docs](https://github.com/kmrgautam18-alt/career-ops-v2/tree/main/docs)
- 🐛 **Issues:** [GitHub Issues](https://github.com/kmrgautam18-alt/career-ops-v2/issues)
- 📧 **Author:** Kumar Gautam — [GitHub](https://github.com/kmrgautam18-alt)
