import os, json, random, requests

SERVICE_URL = os.getenv("CGOL_SERVICE_URL", "http://127.0.0.1:8000")

def simulate_word(word: str):
    r = requests.post(f"{SERVICE_URL}/simulate", json={"word": word}, timeout=30)
    r.raise_for_status()
    return r.json()

def tool_schema():
    return {
        "name": "conway_simulator",
        "description": "Simulate Conway's Game of Life seeded from an ASCII word.",
        "parameters": {
            "type": "object",
            "properties": {
                "word": {"type": "string", "description": "ASCII word to simulate"}
            },
            "required": ["word"]
        }
    }

# Simple prompt router that answers the two required prompts
def handle_prompt(prompt: str) -> str:
    p = prompt.lower()
    if "how many generations" in p and "conway" in p and "word" in p:
        import re
        m = re.search(r"[‘'“\"]([^’'”\"]+)[’'”\"]", prompt)  # grab word between quotes if present
        word = m.group(1) if m else prompt.split()[-1]
        data = simulate_word(word)
        return f"Word: {word}\nGenerations: {data['generations']}\nScore: {data['score']}\nReason: {data['termination_reason']}" + (f" (period={data['period']})" if data.get('period') else "")
    if "generate" in p and "random words" in p and "highest conway score" in p:
        import re
        m = re.search(r"generate\s+(\d+)\s+random", p)
        n = int(m.group(1)) if m else 3
        words = ["".join(random.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(random.randint(3,8))) for _ in range(n)]
        results = [(w, simulate_word(w)) for w in words]
        best = max(results, key=lambda t: t[1]["score"])
        lines = ["Results:"] + [f"- {w}: score={r['score']}, generations={r['generations']}" for w, r in results]
        lines.append(f"Best: {best[0]} (score={best[1]['score']})")
        return "\n".join(lines)
    # JSON fallback: if LLM sends {"word": "..."}
    try:
        payload = json.loads(prompt)
        if isinstance(payload, dict) and "word" in payload:
            return json.dumps(simulate_word(payload["word"]))
    except Exception:
        pass
    return "Try: 'How many generations will the word \"monument\" return from the Conway tool?'"
