#!/bin/bash
# ==========================================
# Career-Ops v2 — RHEL 10.2 / Fedora 40+
# Automated Deployment Script
# ==========================================
# Run this on your RHEL VM as root or with sudo.
#
# Usage:
#   sudo bash scripts/deploy-rhel.sh
# ==========================================

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

log()  { echo -e "${GREEN}[✓]${NC} $1"; }
warn() { echo -e "${YELLOW}[!]${NC} $1"; }
err()  { echo -e "${RED}[✗]${NC} $1"; }
info() { echo -e "${CYAN}[i]${NC} $1"; }

echo ""
echo "=============================================="
echo "  Career-Ops v2 — RHEL Deployment"
echo "=============================================="
echo ""

# ---------- Root check ----------
if [ "$(id -u)" -ne 0 ]; then
  err "Please run as root: sudo bash $0"
  exit 1
fi

# ---------- Step 1: System Update ----------
info "Step 1/8: Updating system packages..."
dnf update -y > /dev/null 2>&1
log "System updated"

# ---------- Step 2: Install Dependencies ----------
info "Step 2/8: Installing dependencies (git, curl, python3, nodejs)..."
dnf install -y git curl python3 python3-pip python3-devel nodejs npm gcc > /dev/null 2>&1
log "Dependencies installed"

# ---------- Step 3: Install Docker ----------
info "Step 3/8: Installing Docker..."
if ! command -v docker &> /dev/null; then
  dnf config-manager --add-repo https://download.docker.com/linux/rhel/docker-ce.repo > /dev/null 2>&1
  dnf install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin > /dev/null 2>&1
  systemctl enable docker --now
  log "Docker installed and started"
else
  log "Docker already installed"
fi

# ---------- Step 4: Add user to docker group ----------
info "Step 4/8: Adding current user to docker group..."
if [ -n "${SUDO_USER:-}" ]; then
  usermod -aG docker "$SUDO_USER"
  log "User $SUDO_USER added to docker group (log out/in to take effect)"
else
  warn "Running as root directly — skipping docker group setup"
fi

# ---------- Step 5: Install Docker Compose ----------
info "Step 5/8: Installing Docker Compose plugin..."
dnf install -y docker-compose-plugin > /dev/null 2>&1 || true
log "Docker Compose ready"

# ---------- Step 6: Clone / Pull the Repo ----------
REPO_DIR="/opt/career-ops"
info "Step 6/8: Setting up project at $REPO_DIR..."

if [ -d "$REPO_DIR" ]; then
  cd "$REPO_DIR"
  git pull origin main
  log "Repository updated"
else
  git clone https://github.com/kmrgautam18-alt/career-ops-v2.git "$REPO_DIR"
  cd "$REPO_DIR"
  log "Repository cloned"
fi

# ---------- Step 7: Configure Environment ----------
info "Step 7/8: Configuring environment variables..."

if [ ! -f "$REPO_DIR/.env" ]; then
  cat > "$REPO_DIR/.env" << 'ENVEOF'
# ==========================================
# Career-Ops v2 — RHEL Production
# ==========================================
APP_NAME=Career-Ops
APP_VERSION=0.1.0
APP_ENV=production
DEBUG=false

DATABASE_URL=postgresql://careerops:ChangeMe123!@postgres:5432/careerops
POSTGRES_DB=careerops
POSTGRES_USER=careerops
POSTGRES_PASSWORD=ChangeMe123!
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20

CORS_ORIGINS=http://localhost,http://localhost:80,http://YOUR_VM_IP
CORS_ALLOW_CREDENTIALS=true

SECRET_KEY=replace-with-openssl-rand-hex-64
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
ENVEOF

  # Generate a random SECRET_KEY
  NEW_SECRET=$(python3 -c "import secrets; print(secrets.token_hex(32))")
  sed -i "s/replace-with-openssl-rand-hex-64/$NEW_SECRET/" "$REPO_DIR/.env"

  log ".env file created with random SECRET_KEY"
  warn "IMPORTANT: Edit $REPO_DIR/.env to change POSTGRES_PASSWORD and CORS_ORIGINS!"
else
  log ".env file already exists"
fi

# ---------- Step 8: Firewall ----------
info "Step 8/8: Configuring firewall..."
if systemctl is-active firewalld &> /dev/null; then
  firewall-cmd --permanent --add-port=80/tcp 2>/dev/null || true
  firewall-cmd --permanent --add-port=443/tcp 2>/dev/null || true
  firewall-cmd --reload 2>/dev/null || true
  log "Firewall: ports 80, 443 opened"
else
  warn "firewalld not active — ensure ports 80/443 are accessible"
fi

# ---------- SELinux ----------
if command -v getenforce &> /dev/null && [ "$(getenforce)" = "Enforcing" ]; then
  warn "SELinux is Enforcing — you may need: setsebool -P httpd_can_network_connect on"
fi

# ---------- Summary ----------
VM_IP=$(hostname -I | awk '{print $1}')
echo ""
echo "=============================================="
echo -e "${GREEN}  ✅ RHEL Setup Complete!${NC}"
echo "=============================================="
echo ""
echo "  Next steps:"
echo ""
echo "  1. Edit the .env file:"
echo "     sudo nano $REPO_DIR/.env"
echo "     (Set POSTGRES_PASSWORD, CORS_ORIGINS to your VM IP)"
echo ""
echo "  2. Start the stack:"
echo "     cd $REPO_DIR"
echo "     docker compose up -d --build"
echo ""
echo "  3. Run database migrations:"
echo "     docker compose exec backend alembic upgrade head"
echo ""
echo "  4. Access the app:"
echo -e "     Frontend: ${CYAN}http://$VM_IP${NC}"
echo -e "     API Docs: ${CYAN}http://$VM_IP:8000/docs${NC}"
echo ""
echo "  5. To stop:"
echo "     cd $REPO_DIR && docker compose down"
echo ""
echo "  6. To update:"
echo "     cd $REPO_DIR && git pull && docker compose up -d --build"
echo ""
echo "=============================================="
