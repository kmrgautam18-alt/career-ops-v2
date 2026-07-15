#!/bin/bash
# ==========================================
# Career-Ops v2 — Dev Preview
# Starts both backend and frontend servers
# for local development.
#
# Usage:
#   bash scripts/preview.sh
#
# Or from project root:
#   bash scripts/preview.sh
# ==========================================

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
BACKEND_PORT="${BACKEND_PORT:-8000}"
FRONTEND_PORT="${FRONTEND_PORT:-5173}"
DATABASE_URL="${DATABASE_URL:-sqlite:///./data/careerops.db}"
SECRET_KEY="${SECRET_KEY:-dev-secret-key-careerops-2026}"

echo "=========================================="
echo "  Career-Ops v2 — Dev Preview"
echo "=========================================="
echo ""

# ---------- Ensure data directory ----------
mkdir -p "$ROOT_DIR/data"

# ---------- Start Backend ----------
echo "[1/2] Starting backend on port $BACKEND_PORT..."
cd "$ROOT_DIR"
DATABASE_URL="$DATABASE_URL" \
SECRET_KEY="$SECRET_KEY" \
nohup python3 -m uvicorn backend.app.main:app \
  --host 0.0.0.0 \
  --port "$BACKEND_PORT" \
  --reload \
  > /tmp/careerops-backend.log 2>&1 &

BACKEND_PID=$!
echo "       PID: $BACKEND_PID"

# Wait for backend to be ready
for i in {1..15}; do
  if curl -s "http://localhost:$BACKEND_PORT/" > /dev/null 2>&1; then
    echo "       Backend is healthy ✓"
    break
  fi
  if [ "$i" -eq 15 ]; then
    echo "       Backend failed to start!"
    kill $BACKEND_PID 2>/dev/null
    exit 1
  fi
  sleep 1
done

# ---------- Frontend ----------
echo "[2/2] Starting frontend on port $FRONTEND_PORT..."
cd "$ROOT_DIR/frontend"
nohup bun dev --port "$FRONTEND_PORT" \
  > /tmp/careerops-frontend.log 2>&1 &

FRONTEND_PID=$!
echo "       PID: $FRONTEND_PID"
sleep 3

# ---------- Summary ----------
echo ""
echo "=========================================="
echo "  ✅ Preview ready!"
echo "=========================================="
echo ""
echo "  Frontend : http://localhost:$FRONTEND_PORT"
echo "  Backend  : http://localhost:$BACKEND_PORT"
echo "  API Docs : http://localhost:$BACKEND_PORT/docs"
echo ""
echo "  Stop with: kill $BACKEND_PID $FRONTEND_PID"
echo "  Or:        pkill -f 'uvicorn' && pkill -f 'vite'"
echo ""
echo "  Logs:"
echo "    Backend  → tail -f /tmp/careerops-backend.log"
echo "    Frontend → tail -f /tmp/careerops-frontend.log"
echo "=========================================="

# Save PIDs for easy cleanup
echo "$BACKEND_PID" > /tmp/careerops-backend.pid
echo "$FRONTEND_PID" > /tmp/careerops-frontend.pid
