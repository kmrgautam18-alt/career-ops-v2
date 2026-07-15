#!/bin/bash
# ==========================================
# Career-Ops v2 — Deploy to EC2
# ==========================================
# Prerequisites:
#   1. Set these env vars or add to your shell:
#      export EC2_HOST="ec2-xx-xx-xx-xx.compute-1.amazonaws.com"
#      export EC2_USER="ubuntu"
#      export EC2_SSH_KEY="/path/to/your-key.pem"
#   2. The .env file must already exist on the server
#
# Usage:
#   ./scripts/deploy-ec2.sh
# ==========================================

set -euo pipefail

EC2_HOST="${EC2_HOST:?Must set EC2_HOST}"
EC2_USER="${EC2_USER:-ubuntu}"
EC2_SSH_KEY="${EC2_SSH_KEY:?Must set EC2_SSH_KEY}"
COMPOSE_FILE="docker-compose.yml"

echo "🚀 Deploying Career-Ops v2 to EC2..."
echo "   Host: $EC2_HOST"
echo "   User: $EC2_USER"
echo ""

# 1. Ensure the remote project directory exists
ssh -i "$EC2_SSH_KEY" "$EC2_USER@$EC2_HOST" "mkdir -p ~/career-ops-v2"

# 2. Copy project files (excluding heavy/unnecessary dirs)
rsync -avz --delete \
  --exclude '.git' \
  --exclude 'node_modules' \
  --exclude '__pycache__' \
  --exclude '*.pyc' \
  --exclude '.venv' \
  --exclude 'venv' \
  --exclude '*.db' \
  --exclude 'data/' \
  -e "ssh -i $EC2_SSH_KEY" \
  ./ "$EC2_USER@$EC2_HOST:~/career-ops-v2/"

# 3. Pull latest images and restart stack
ssh -i "$EC2_SSH_KEY" "$EC2_USER@$EC2_HOST" \
  "cd ~/career-ops-v2 && \
   docker compose pull && \
   docker compose up -d --build && \
   echo '✅ Stack restarted'"

# 4. Run database migrations
ssh -i "$EC2_SSH_KEY" "$EC2_USER@$EC2_HOST" \
  "cd ~/career-ops-v2 && \
   docker compose exec -T backend alembic upgrade head && \
   echo '✅ Migrations applied'"

echo ""
echo "✅ Deployment complete!"
echo "   Frontend: http://$EC2_HOST"
echo "   API:      http://$EC2_HOST:8000"
echo "   Docs:     http://$EC2_HOST:8000/docs"
