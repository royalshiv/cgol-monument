#!/bin/bash
set -e

echo "🚀 Starting CGOL Monument..."

# 1. Create venv if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv .venv
fi

# 2. Activate venv (Git Bash / Linux / Mac)
source .venv/Scripts/activate 2>/dev/null || source .venv/bin/activate

# 3. Install dependencies
echo "📥 Installing dependencies..."
python -m pip install --upgrade pip
pip install -r requirements.txt

# (optional) self-heal Streamlit
if ! command -v streamlit >/dev/null 2>&1; then
  echo "📦 Installing Streamlit..."
  pip install streamlit openai
fi

# 4. Start backend
echo "🖥️  Starting backend on http://127.0.0.1:8000 ..."
uvicorn server.app:app --reload --port 8000 &
BACKEND_PID=$!

# 5. Wait briefly so ports are ready
sleep 3

# 6. Start UI
echo "🌐 Starting UI..."
export PYTHONPATH=.
streamlit run ui/app.py

# 7. Cleanup on exit
trap "kill $BACKEND_PID" EXIT

# 1) Ensure correct shebang is at the very top of run.sh:
#    It should be exactly this as the first line:
#    #!/bin/bash
sed -n '1p' run.sh

# If it's not, open and edit:
code run.sh
# (put: #!/bin/bash on line 1, save)

# 2) Convert Windows CRLF -> LF (prevents /bin/bash^M errors)
sudo apt-get update && sudo apt-get install -y dos2unix
dos2unix run.sh

# 3) Make it executable
chmod +x run.sh

# 4) Run it
./run.sh
# or (works even without +x)
bash run.sh
