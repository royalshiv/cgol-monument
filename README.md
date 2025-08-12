# 🕹 CGOL Monument Challenge

A complete solution for the **Monument AI - Programming Challenge (SEGA, August 2025)**.  
Implements a RESTful backend for a variation of **Conway’s Game of Life**, a Python client tool for LLM integration, and a Streamlit UI for easy interaction.

---

## 📜 Features

### Backend (FastAPI)
- Accepts an English word (mixed case allowed).
- Converts it to ASCII binary bitmask as the initial seed.
- Uses a **60 x 40** grid.
- Runs Conway's Game of Life until:
  - Extinction
  - Persistent state
  - Constant periodic pattern (< 10 generations)
  - Or **max 1000 generations**
- Returns:
  - **Generations** until stability
  - **Score** = total number of cells spawned during execution.

### Python Client Tool
- Callable by `gpt-4o-mini` or other LLMs.
- Handles:
  - “How many generations will the word ‘monument’ return from the Conway tool?”
  - “Generate 3 random words and tell me the highest Conway score.”

### Streamlit UI
- Simple web interface to:
  - Query the backend directly
  - Send natural language prompts to the LLM-bound Conway tool.

---

## 🚀 Quick Start (Recommended)

After cloning the repo, run **everything** (backend + UI) with one command:

```bash
./run.sh

This will:

1. Create a virtual environment (if missing)
2. Install dependencies
3. Start the FastAPI backend
4. Launch the Streamlit UI in your browser

---

🛠 **Manual Setup** (If you prefer step-by-step)

1️⃣ **Clone the repo**
```bash
git clone https://github.com/royalshiv/cgol-monument.git
cd cgol-monument

2️⃣ Create and activate a virtual environment
python -m venv .venv
source .venv/Scripts/activate

3️⃣ Install dependencies

python -m pip install --upgrade pip
pip install -r requirements.txt

4️⃣ Run the backend
uvicorn server.app:app --reload --port 8000
Visit: 'http://127.0.0.1:8000/healthz' to check status.

5️⃣ Run the UI (in another terminal)
export PYTHONPATH=.      # Git Bash / Mac
# set PYTHONPATH=.       # PowerShell
streamlit run ui/app.py

📂 Project Structure

cgol-monument/
├── client/               # Python tool callable by LLM
│   ├── __init__.py
│   └── conway_tool.py
├── server/               # FastAPI backend
│   ├── app.py
│   ├── cgol.py
│   ├── models.py
│   └── __init__.py
├── ui/                   # Streamlit UI
│   └── app.py
├── tests/                # Unit tests
├── run.sh                # One-command startup script
├── requirements.txt
└── README.md
