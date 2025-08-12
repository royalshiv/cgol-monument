#!/bin/bash
set -e  # Exit on error

echo "🚀 Starting CGOL Monument..."

# 1. Create venv if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv .venv
fi

# 2. Activate venv (Git Bash / Linux / Mac style)
source .venv/Scripts/activate 2>/dev/null || source .venv/bin/activate

# 3. Install dependencies
echo "📥 Installing dependencies..."
python -m pip install --upgrade pip
pip install -r requirements.txt

# 4. Start backend in background
echo "🖥️  Starting backend on http://127.0.0.1:8000 ..."
uvicorn server.app:app --reload --port 8000 &
BACKEND_PID=$!

# 5. Wait a bit for backend to start
sleep 3

# 6. Start UI (Streamlit)
echo "🌐 Starting UI..."
export PYTHONPATH=.
streamlit run ui/app.py

# 7. Cleanup backend on exit
trap "kill $BACKEND_PID" EXIT
