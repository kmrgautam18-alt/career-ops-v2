#!/bin/bash
# ==========================================
# Career-Ops v2 — EC2 Bootstrap Script
# Run this as EC2 user-data or SSH into the
# instance and execute manually.
# ==========================================

set -euo pipefail

# ---------- Update system ----------
sudo apt-get update -y
sudo apt-get upgrade -y

# ---------- Install Docker ----------
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu
sudo systemctl enable docker
sudo systemctl start docker

# ---------- Install Docker Compose ----------
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# ---------- Clone the repo ----------
cd /home/ubuntu
git clone https://github.com/kmrgautam18-alt/career-ops-v2.git
cd career-ops-v2

# ---------- Create .env from template ----------
cp .env.example .env
# IMPORTANT: Edit .env with your production values:
#   nano .env
# Then run:
#   docker compose up -d --build
#   docker compose exec backend alembic upgrade head

echo "=========================================="
echo "Career-Ops EC2 bootstrap complete!"
echo ""
echo "Next steps (SSH into the instance):"
echo "  1. cd ~/career-ops-v2"
echo "  2. nano .env              # Set secrets"
echo "  3. docker compose up -d --build"
echo "  4. docker compose exec backend alembic upgrade head"
echo ""
echo "  Frontend: http://$(curl -s http://checkip.amazonaws.com)"
echo "  Backend:  http://$(curl -s http://checkip.amazonaws.com):8000"
echo "  Docs:     http://$(curl -s http://checkip.amazonaws.com):8000/docs"
echo "=========================================="
