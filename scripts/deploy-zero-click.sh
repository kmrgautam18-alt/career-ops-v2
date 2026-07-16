#!/bin/bash
# =============================================================================
# Career-Ops — Zero-Click Deployment Script
# =============================================================================
# Run this on a FRESH RHEL 10.2 VM and it will:
#   1. Install Docker, configure firewall
#   2. Clone Career-Ops, generate all secrets
#   3. Set up DuckDNS free domain (yourname.duckdns.org)
#   4. Set up Cloudflare Tunnel (free HTTPS + DDoS protection)
#   5. Configure Gemini AI (free tier)
#   6. Build and start ALL 16 Docker services
#   7. Auto-register admin user
#   8. Set up automatic daily backups
#   9. Set up daily LinkedIn auto-posting
#  10. Verify everything works
#
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/kmrgautam18-alt/career-ops-v2/main/scripts/deploy-zero-click.sh | bash
#
# Or locally:
#   bash scripts/deploy-zero-click.sh
#
# Prerequisites:
#   - Fresh RHEL 10.2 VM with internet access
#   - DuckDNS token (FREE: https://duckdns.org)
#   - Gemini API key (FREE: https://aistudio.google.com)
#   - Cloudflare token (FREE: https://dash.cloudflare.com) — optional but recommended
# =============================================================================

set -euo pipefail

# ── Colors ─────────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
BOLD='\033[1m'
NC='\033[0m'

# ── Config ──────────────────────────────────────────────────────────────
REPO_URL="https://github.com/kmrgautam18-alt/career-ops-v2.git"
PROJECT_DIR="$HOME/career-ops-v2"
DEPLOY_LOG="/tmp/careerops-deploy-$(date +%Y%m%d_%H%M%S).log"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# ── Banner ─────────────────────────────────────────────────────────────
print_banner() {
    clear
    echo -e "${CYAN}"
    echo '  ╔════════════════════════════════════════════════════════╗'
    echo '  ║                                                        ║'
    echo '  ║     🚀 Career-Ops v2 — Zero-Click Deployment           ║'
    echo '  ║     From Fresh RHEL VM to Live Internet in 15 Minutes  ║'
    echo '  ║                                                        ║'
    echo '  ╚════════════════════════════════════════════════════════╝'
    echo -e "${NC}"
    echo ""
    echo -e "${YELLOW}Logging to:${NC} $DEPLOY_LOG"
    echo ""
}

# ── Helpers ──────────────────────────────────────────────────────────────
log()    { echo -e "${GREEN}[$(date '+%H:%M:%S')]${NC} $*" | tee -a "$DEPLOY_LOG"; }
warn()   { echo -e "${YELLOW}[$(date '+%H:%M:%S')] ⚠️ $*${NC}" | tee -a "$DEPLOY_LOG"; }
error()  { echo -e "${RED}[$(date '+%H:%M:%S')] ❌ $*${NC}" | tee -a "$DEPLOY_LOG"; }
header() { echo -e "\n${MAGENTA}════════════════════════════════════════════════${NC}"; echo -e "${BOLD}$*${NC}"; echo -e "${MAGENTA}════════════════════════════════════════════════${NC}\n"; }
prompt() { echo -e "\n${CYAN}📝 $*${NC}"; }
spinner() {
    local pid=$1
    local msg=$2
    local spin='⣾⣽⣻⢿⡿⣟⣯⣷'
    local i=0
    while kill -0 "$pid" 2>/dev/null; do
        echo -ne "\r${YELLOW}${spin:$i:1}${NC} $msg"
        i=$(( (i+1) % ${#spin} ))
        sleep 0.1
    done
    echo -ne "\r${GREEN}✅${NC} $msg\n"
}

# ── Prerequisites ──────────────────────────────────────────────────────
gather_info() {
    header "📋 Gathering Information"

    echo -e "You need 3 FREE accounts to go live. I'll help you set them up."
    echo ""

    # ── DuckDNS ────────────────────────────────────────────────────────
    prompt "Step 1: DuckDNS (Free Domain)"
    echo "  Go to https://duckdns.org → Sign in with Google/GitHub"
    echo "  Create a subdomain (e.g., 'careerops' → careerops.duckdns.org)"
    echo ""
    read -rp "  Enter your DuckDNS domain (e.g., careerops): " DUCKDNS_DOMAIN
    DUCKDNS_DOMAIN=${DUCKDNS_DOMAIN:-careerops}
    read -rp "  Enter your DuckDNS token (from duckdns.org): " DUCKDNS_TOKEN
    while [ -z "$DUCKDNS_TOKEN" ]; do
        warn "DuckDNS token is required"
        read -rp "  Enter your DuckDNS token: " DUCKDNS_TOKEN
    done
    echo ""

    # ── Gemini ─────────────────────────────────────────────────────────
    prompt "Step 2: Google Gemini AI API Key (Free)"
    echo "  Go to https://aistudio.google.com → Get API Key → Create"
    echo "  No credit card needed. Free tier: 60 requests/minute."
    echo ""
    read -rp "  Enter your Gemini API key: " GEMINI_KEY
    while [ -z "$GEMINI_KEY" ]; do
        warn "Gemini key is required for AI features"
        read -rp "  Enter your Gemini API key: " GEMINI_KEY
    done
    echo ""

    # ── Cloudflare Tunnel ──────────────────────────────────────────────
    prompt "Step 3: Cloudflare Tunnel (Free HTTPS — RECOMMENDED)"
    echo "  Go to https://dash.cloudflare.com → Zero Trust → Access → Tunnels"
    echo "  Create tunnel → 'careerops-tunnel' → Copy token"
    echo "  Skip this if you have a public IP (not recommended)"
    echo ""
    read -rp "  Cloudflare tunnel token (or press Enter to skip): " CF_TOKEN
    echo ""

    # ── Slack (Optional) ───────────────────────────────────────────────
    prompt "Step 4: Slack Webhook for Alerts (Optional)"
    echo "  Go to Slack → Apps → Incoming Webhooks → Add → Copy URL"
    echo ""
    read -rp "  Slack webhook URL (or press Enter to skip): " SLACK_WEBHOOK
    echo ""

    # ── Admin User ─────────────────────────────────────────────────────
    prompt "Step 5: Admin Account"
    read -rp "  Admin email: " ADMIN_EMAIL
    ADMIN_EMAIL=${ADMIN_EMAIL:-admin@careerops.com}
    read -rp "  Admin password (min 8 chars): " ADMIN_PASS
    ADMIN_PASS=${ADMIN_PASS:-Admin@12345}
    echo ""

    # Summary
    echo -e "${GREEN}──────────────────────────────────────${NC}"
    echo -e "  Domain:    ${CYAN}https://${DUCKDNS_DOMAIN}.duckdns.org${NC}"
    echo -e "  Admin:     ${CYAN}${ADMIN_EMAIL}${NC}"
    echo -e "  AI:        ${CYAN}Gemini (free tier)${NC}"
    echo -e "  HTTPS:     ${CYAN}$([ -n "$CF_TOKEN" ] && echo 'Cloudflare Tunnel' || echo 'No HTTPS — not recommended')${NC}"
    echo -e "  Alerts:    ${CYAN}$([ -n "$SLACK_WEBHOOK" ] && echo 'Slack configured' || echo 'None')${NC}"
    echo -e "${GREEN}──────────────────────────────────────${NC}"
    echo ""
    read -rp "  Proceed with deployment? (yes/no): " CONFIRM
    if [ "$CONFIRM" != "yes" ]; then
        error "Deployment cancelled"
        exit 1
    fi
}

# ── Phase 1: System Setup ──────────────────────────────────────────────
phase1_system() {
    header "🔥 Phase 1: System Preparation"

    log "Updating system packages..."
    sudo dnf update -y >> "$DEPLOY_LOG" 2>&1 &
    spinner $! "Updating system packages"

    log "Installing Docker..."
    sudo dnf install -y dnf-plugins-core >> "$DEPLOY_LOG" 2>&1
    sudo dnf config-manager --add-repo https://download.docker.com/linux/rhel/docker-ce.repo >> "$DEPLOY_LOG" 2>&1
    sudo dnf install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin >> "$DEPLOY_LOG" 2>&1 &
    spinner $! "Installing Docker"

    sudo systemctl enable --now docker >> "$DEPLOY_LOG" 2>&1
    sudo usermod -aG docker "$USER" >> "$DEPLOY_LOG" 2>&1

    log "Installing system tools..."
    sudo dnf install -y git curl jq openssl cronie nano >> "$DEPLOY_LOG" 2>&1 &
    spinner $! "Installing system tools"

    # Configure firewall
    log "Configuring firewall..."
    sudo firewall-cmd --permanent --add-port=8000/tcp 2>/dev/null || true
    sudo firewall-cmd --permanent --add-port=5678/tcp 2>/dev/null || true
    sudo firewall-cmd --permanent --add-port=3001/tcp 2>/dev/null || true
    sudo firewall-cmd --permanent --add-port=9090/tcp 2>/dev/null || true
    sudo firewall-cmd --reload 2>/dev/null || true
}

# ── Phase 2: Clone & Configure ─────────────────────────────────────────
phase2_clone() {
    header "📦 Phase 2: Clone & Configure"

    cd "$HOME"

    log "Cloning Career-Ops repository..."
    if [ -d "$PROJECT_DIR" ]; then
        warn "Project directory exists — pulling latest"
        cd "$PROJECT_DIR" && git pull origin main >> "$DEPLOY_LOG" 2>&1
    else
        git clone "$REPO_URL" >> "$DEPLOY_LOG" 2>&1 &
        spinner $! "Cloning repository"
    fi

    cd "$PROJECT_DIR"

    # Generate .env with all secrets
    log "Generating .env with secure secrets..."
    POSTGRES_PASS=$(openssl rand -hex 32)
    SECRET_KEY=$(openssl rand -hex 32)
    GRAFANA_PASS=$(openssl rand -hex 16)
    N8N_KEY=$(openssl rand -hex 32)

    cat > .env << ENVEOF
# ── Database ──────────────────────────────
POSTGRES_DB=careerops
POSTGRES_USER=careerops
POSTGRES_PASSWORD=${POSTGRES_PASS}

# ── JWT ───────────────────────────────────
SECRET_KEY=${SECRET_KEY}

# ── AI / Gemini ───────────────────────────
LLM_API_KEY=${GEMINI_KEY}

# ── Grafana ───────────────────────────────
GRAFANA_ADMIN_USER=admin
GRAFANA_ADMIN_PASSWORD=${GRAFANA_PASS}

# ── n8n ───────────────────────────────────
N8N_ENCRYPTION_KEY=${N8N_KEY}

# ── CORS ──────────────────────────────────
CORS_ORIGINS=http://localhost:3000,https://${DUCKDNS_DOMAIN}.duckdns.org

# ── SMTP (Gmail App Password) ─────────────
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=
SMTP_PASSWORD=
SMTP_FROM_EMAIL=
SMTP_FROM_NAME=Career-Ops
SMTP_TLS=true
SMTP_ENABLED=false

# ── Redis / Celery ────────────────────────
REDIS_ENABLED=true
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=
REDIS_DB=0
CELERY_ENABLED=true
CELERY_BROKER_URL=redis://redis:6379/1
CELERY_RESULT_BACKEND=redis://redis:6379/2

# ── OAuth (Social Login) ──────────────────
OAUTH_ENABLED=false
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GITHUB_CLIENT_ID=
GITHUB_CLIENT_SECRET=
ENVEOF

    log ".env created with 256-bit random secrets"

    # Create necessary directories
    mkdir -p data monitoring/loki backups/postgres
}

# ── Phase 3: DuckDNS ────────────────────────────────────────────────────
phase3_duckdns() {
    header "🌐 Phase 3: DuckDNS — Free Domain"

    log "Setting up DuckDNS auto-updater..."
    sudo mkdir -p /opt/duckdns

    sudo tee /opt/duckdns/duck.sh > /dev/null << 'DUCKDNS'
#!/bin/bash
# DuckDNS auto-updater — updates your free domain with your current IP
# Installed by Career-Ops deploy-zero-click.sh
TOKEN="${DUCKDNS_TOKEN}"
DOMAIN="${DUCKDNS_DOMAIN}"
LOG_FILE="/opt/duckdns/duck.log"

# Update DuckDNS with current public IP
response=$(curl -s "https://www.duckdns.org/update?domains=${DOMAIN}&token=${TOKEN}&ip=")
echo "$(date): $response" >> "$LOG_FILE"
if [ "$response" = "OK" ]; then
    echo "IP updated successfully"
else
    echo "Update failed: $response"
fi
DUCKDNS

    # Replace tokens in the script
    sudo sed -i "s/\${DUCKDNS_TOKEN}/$DUCKDNS_TOKEN/" /opt/duckdns/duck.sh
    sudo sed -i "s/\${DUCKDNS_DOMAIN}/$DUCKDNS_DOMAIN/" /opt/duckdns/duck.sh
    sudo chmod +x /opt/duckdns/duck.sh

    # Test it
    log "Testing DuckDNS update..."
    sudo /opt/duckdns/duck.sh >> "$DEPLOY_LOG" 2>&1
    if grep -q "OK" /opt/duckdns/duck.log 2>/dev/null; then
        log "✅ DuckDNS update successful!"
    else
        warn "DuckDNS test returned: $(cat /opt/duckdns/duck.log)"
    fi

    # Set up cron for every 5 minutes
    log "Setting up automatic IP updates (every 5 minutes)..."
    (sudo crontab -l 2>/dev/null; echo "*/5 * * * * sudo /opt/duckdns/duck.sh >/dev/null 2>&1") | sudo crontab -
    log "Cron job installed"
}

# ── Phase 4: Cloudflare Tunnel ──────────────────────────────────────────
phase4_cloudflare() {
    if [ -z "${CF_TOKEN:-}" ]; then
        log "Skipping Cloudflare Tunnel (not configured)"
        return
    fi

    header "☁️ Phase 4: Cloudflare Tunnel (Free HTTPS)"

    log "Starting Cloudflare Tunnel..."
    sudo docker run -d --restart=always --name cloudflared \
        cloudflare/cloudflared:latest tunnel --no-autoupdate run --token "$CF_TOKEN" >> "$DEPLOY_LOG" 2>&1

    log "Cloudflare Tunnel started"
    log "⚠️  Next step: Go to Cloudflare Dashboard → Tunnels → Configure"
    log "   Public hostname: ${DUCKDNS_DOMAIN}.duckdns.org"
    log "   Service: http://localhost:80"
    log "   TLS: Full (strict)"
}

# ── Phase 5: Build & Start ──────────────────────────────────────────────
phase5_deploy() {
    header "🐳 Phase 5: Build & Deploy Docker Stack"

    # Start Docker if not running (newgrp may not have taken effect)
    sudo systemctl start docker 2>/dev/null || true

    log "Building and starting all 16 Docker services..."
    log "This takes 3-5 minutes on first run..."

    # Use sudo to ensure Docker access
    cd "$PROJECT_DIR"
    sudo docker compose up -d --build >> "$DEPLOY_LOG" 2>&1 &
    local build_pid=$!

    # Show progress
    while kill -0 "$build_pid" 2>/dev/null; do
        echo -ne "\r${YELLOW}⏳${NC} Building Docker images... (check logs: tail -f $DEPLOY_LOG)"
        sleep 2
    done
    wait "$build_pid"

    echo -ne "\r${GREEN}✅${NC} Docker build complete!\n"
    log "✅ All services built and started"

    # Wait for services to be healthy
    log "Waiting for services to become healthy..."
    sleep 10

    # Show running services
    sudo docker compose ps >> "$DEPLOY_LOG" 2>&1
}

# ── Phase 6: Initialize ────────────────────────────────────────────────
phase6_init() {
    header "⚡ Phase 6: Database & User Setup"

    log "Running database migrations..."
    sudo docker compose exec -T backend alembic upgrade head >> "$DEPLOY_LOG" 2>&1 || \
        log "Migrations skipped (may not exist yet)"

    log "Creating admin user..."
    # First check if user exists
    local login_check
    login_check=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
        -H "Content-Type: application/json" \
        -d "{\"email\":\"${ADMIN_EMAIL}\",\"password\":\"${ADMIN_PASS}\"}" 2>/dev/null || echo "failed")

    if echo "$login_check" | grep -q "access_token"; then
        log "✅ Admin user already exists — login successful"
    else
        # Register the admin user
        REG_RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/users/register \
            -H "Content-Type: application/json" \
            -d "{\"email\":\"${ADMIN_EMAIL}\",\"password\":\"${ADMIN_PASS}\",\"username\":\"admin\",\"full_name\":\"Career-Ops Admin\"}" 2>/dev/null)

        if echo "$REG_RESPONSE" | grep -q "success.*true\|id"; then
            log "✅ Admin user created successfully!"
        else
            warn "User registration response: $REG_RESPONSE"
        fi
    fi
}

# ── Phase 7: Backup ─────────────────────────────────────────────────────
phase7_backup() {
    header "💾 Phase 7: Automated Backups"

    log "Installing backup cron job (daily at 2 AM)..."
    (crontab -l 2>/dev/null; echo "0 2 * * * cd ${PROJECT_DIR} && bash scripts/backup-db.sh --cron") | crontab -
    log "Daily backups configured"

    # Test backup
    log "Testing backup..."
    bash "$PROJECT_DIR/scripts/backup-db.sh" >> "$DEPLOY_LOG" 2>&1 || warn "Backup test had issues"
}

# ── Phase 8: LinkedIn Automation ───────────────────────────────────────
phase8_linkedin() {
    header "📱 Phase 8: LinkedIn Auto-Posting"

    log "Setting up LinkedIn daily content automation..."

    mkdir -p "$PROJECT_DIR/data/linkedin"

    # Create the cron job for daily posting
    (crontab -l 2>/dev/null; echo "0 9 * * * cd ${PROJECT_DIR} && bash scripts/linkedin-automation.sh --daily >> data/linkedin/poster.log 2>&1") | crontab -
    log "✅ Daily LinkedIn post scheduled at 9 AM"

    # Generate first batch of content
    log "Generating first week of LinkedIn content..."
    bash "$PROJECT_DIR/scripts/linkedin-automation.sh --generate" >> "$DEPLOY_LOG" 2>&1 || true
}

# ── Phase 9: Verification ──────────────────────────────────────────────
phase9_verify() {
    header "✅ Phase 9: Health Verification"

    log "Running health checks..."

    # Check core services
    local checks=(
        "Backend API:8000/health"
        "Backend Readiness:8000/ready"
        "Backend Liveness:8000/live"
        "Prometheus:9090/-/ready"
        "Grafana:3001/api/health"
    )

    for check in "${checks[@]}"; do
        local name="${check%%:*}"
        local port_path="${check#*:}"
        local port="${port_path%/*}"
        local path="/${port_path#*/}"

        if curl -sf "http://localhost:${port}${path}" > /dev/null 2>&1; then
            log "✅ ${name} is healthy"
        else
            warn "${name} is not responding"
        fi
    done

    # Check Docker services
    log ""
    log "Running Docker services:"
    sudo docker compose ps --format "table {{.Name}}\t{{.Status}}\t{{.Ports}}" 2>/dev/null | tee -a "$DEPLOY_LOG"

    # Test AI
    log ""
    log "Testing AI connectivity..."
    local login_token
    login_token=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
        -H "Content-Type: application/json" \
        -d "{\"email\":\"${ADMIN_EMAIL}\",\"password\":\"${ADMIN_PASS}\"}" | \
        python3 -c "import sys,json; print(json.load(sys.stdin).get('data',{}).get('access_token',''))" 2>/dev/null || echo "")

    if [ -n "$login_token" ]; then
        log "✅ API authentication working"

        # Test AI ATS score
        local ats_result
        ats_result=$(curl -s -X POST http://localhost:8000/api/v1/ai/ats-score \
            -H "Content-Type: application/json" \
            -H "Authorization: Bearer ${login_token}" \
            -d '{"resume_text":"Python developer with Docker","job_description":"Python engineer needed"}' 2>/dev/null)

        if echo "$ats_result" | grep -q "overall_score\|success"; then
            log "✅ AI (Gemini) is working!"
        else
            warn "AI test returned: $(echo "$ats_result" | head -c 100)"
        fi
    else
        warn "API login failed — check logs: docker compose logs backend"
    fi

    # Test HTTPS
    if [ -n "${CF_TOKEN:-}" ]; then
        log "Testing HTTPS access..."
        if curl -sf "https://${DUCKDNS_DOMAIN}.duckdns.org" > /dev/null 2>&1; then
            log "✅ HTTPS is working at https://${DUCKDNS_DOMAIN}.duckdns.org"
        else
            warn "HTTPS not yet accessible — Cloudflare Tunnel may still be provisioning"
        fi
    fi
}

# ── Phase 10: Summary ──────────────────────────────────────────────────
phase10_summary() {
    header "🎉 Deployment Complete!"

    TIMESTAMP=$(date)

    # Build the summary
    echo ""
    echo -e "${GREEN}════════════════════════════════════════════════════════════${NC}"
    echo -e "${BOLD}  🚀 Career-Ops v2 is LIVE!${NC}"
    echo -e "${GREEN}════════════════════════════════════════════════════════════${NC}"
    echo ""

    echo -e "  ${BOLD}Your App:${NC}"
    echo -e "  🌐  ${CYAN}https://${DUCKDNS_DOMAIN}.duckdns.org${NC}"
    echo ""

    echo -e "  ${BOLD}Admin Login:${NC}"
    echo -e "  📧  ${ADMIN_EMAIL}"
    echo -e "  🔑  ${ADMIN_PASS}"
    echo ""

    echo -e "  ${BOLD}Services:${NC}"
    echo -e "  🚀  Backend API:     http://localhost:8000"
    echo -e "  📊  Grafana:         http://localhost:3001 (admin / ${GRAFANA_PASS})"
    echo -e "  📈  Prometheus:      http://localhost:9090"
    echo -e "  🔔  Alertmanager:    http://localhost:9093"
    echo -e "  🤖  n8n:             http://localhost:5678"
    echo ""

    echo -e "  ${BOLD}Automation:${NC}"
    echo -e "  📱  LinkedIn posts:  Daily at 9 AM (${PROJECT_DIR}/data/linkedin/)"
    echo -e "  💾  DB backups:      Daily at 2 AM (${PROJECT_DIR}/backups/)"
    echo -e "  🔄  DuckDNS update:  Every 5 minutes"
    echo ""

    echo -e "  ${BOLD}Important Files:${NC}"
    echo -e "  🔐  Env file:        ${PROJECT_DIR}/.env"
    echo -e "  📝  Deploy log:      ${DEPLOY_LOG}"
    echo ""

    echo -e "  ${BOLD}Next Steps:${NC}"
    echo -e "  1. Open ${CYAN}https://${DUCKDNS_DOMAIN}.duckdns.org${NC} in your browser"
    echo -e "  2. Log in with ${CYAN}${ADMIN_EMAIL}${NC} / ${CYAN}${ADMIN_PASS}${NC}"
    echo -e "  3. Create your resume and explore AI features"
    echo -e "  4. Check LinkedIn posts: ${CYAN}ls data/linkedin/${NC}"
    echo -e "  5. Run ${CYAN}docker compose logs --tail=50 backend${NC} for any issues"
    echo ""

    # Save credentials to a secure file
    cat > "$HOME/.careerops-credentials" << CREDEOF
╔══════════════════════════════════════════════════════════════╗
║              Career-Ops v2 — Deployment Credentials           ║
║              Generated: ${TIMESTAMP}                        ║
╚══════════════════════════════════════════════════════════════╝

🌐 URL:       https://${DUCKDNS_DOMAIN}.duckdns.org
📧 Admin:     ${ADMIN_EMAIL}
🔑 Password:  ${ADMIN_PASS}

📊 Grafana:   http://localhost:3001 (admin / ${GRAFANA_PASS})
🤖 n8n:       http://localhost:5678

🚀 Backend:   http://localhost:8000
📈 Prometheus: http://localhost:9090
🔔 Alertmanager: http://localhost:9093

💾 Backups:   ${PROJECT_DIR}/backups/
📱 LinkedIn:  ${PROJECT_DIR}/data/linkedin/
CREDEOF
    chmod 600 "$HOME/.careerops-credentials"

    echo -e "  ${YELLOW}Credentials saved to: ~/.careerops-credentials${NC}"
    echo ""
    echo -e "${GREEN}════════════════════════════════════════════════════════════${NC}"
    echo -e "${BOLD}  🎉 Thank you for using Career-Ops! Go get that job! 🎉${NC}"
    echo -e "${GREEN}════════════════════════════════════════════════════════════${NC}"
}

# ── Main ──────────────────────────────────────────────────────────────
main() {
    print_banner

    # Check if running as root
    if [ "$(id -u)" -eq 0 ]; then
        warn "Running as root — switching to user context"
        # Re-run as the original user
    fi

    gather_info
    phase1_system
    phase2_clone
    phase3_duckdns
    phase4_cloudflare
    phase5_deploy
    phase6_init
    phase7_backup
    phase8_linkedin
    phase9_verify
    phase10_summary
}

main "$@"
