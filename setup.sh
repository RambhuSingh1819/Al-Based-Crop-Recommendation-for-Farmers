#!/usr/bin/env bash
set -euo pipefail

# Resolve project root (folder where this script lives)
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo ""
echo "==============================="
echo "  🚀 Farm Advisor – Setup & Run"
echo "==============================="
echo ""

# -------------------------
# Python binary detection
# -------------------------
# Use PYTHON_BIN if set, otherwise default to python3
PYTHON_BIN="${PYTHON_BIN:-python3}"

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  echo "❌ Could not find '$PYTHON_BIN' on your PATH."
  echo "   Install Python 3, or run like: PYTHON_BIN=python3 ./setup.sh"
  exit 1
fi

echo "🐍 Using Python binary: $PYTHON_BIN"
echo ""

# -------------------------
# Hugging Face model config
# -------------------------
HF_MODEL_DEFAULT_ID="google/vit-base-patch16-224"
export HF_MODEL_ID="${HF_MODEL_ID:-$HF_MODEL_DEFAULT_ID}"

echo "🔐 [Backend] Using Hugging Face model: $HF_MODEL_ID"
echo ""

# -------------------------
# Backend setup & start
# -------------------------
echo "🔧 [Backend] Setting up virtual environment..."
cd "$ROOT_DIR/backend"

if [ ! -d "venv" ]; then
    echo "🧪 [Backend] Creating virtual environment (venv)..."
    "$PYTHON_BIN" -m venv venv
fi

# Activate venv
# shellcheck disable=SC1091
source venv/bin/activate

if [ -f "requirements.txt" ]; then
    echo "📦 [Backend] Installing Python dependencies from requirements.txt..."
    "$PYTHON_BIN" -m pip install --upgrade pip
    "$PYTHON_BIN" -m pip install -r requirements.txt
else
    echo "⚠️ [Backend] requirements.txt not found, skipping pip install."
fi

echo "▶️ [Backend] Starting Uvicorn (http://localhost:8000)..."
uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

echo "✅ [Backend] Running with PID: $BACKEND_PID"
echo ""

# -------------------------
# Frontend setup & start
# -------------------------
echo "🔧 [Frontend] Installing npm dependencies..."
cd "$ROOT_DIR/frontend"

if [ -f "package.json" ]; then
    npm install
else
    echo "❌ [Frontend] package.json not found!"
    kill "$BACKEND_PID" || true
    exit 1
fi

echo "▶️ [Frontend] Starting dev server (usually http://localhost:3000)..."
echo "   Press Ctrl+C to stop the frontend. Backend will be stopped automatically."

npm start

echo ""
echo "⏹ [Frontend] Stopped. Killing backend server..."
kill "$BACKEND_PID" || true
echo "✅ All done. Bye! 👋"
