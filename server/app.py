from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .cgol import run_until_stable
from .models import SimulateRequest, SimulateResponse

app = FastAPI(title="CGOL Service", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}

@app.post("/simulate", response_model=SimulateResponse)
async def simulate(req: SimulateRequest):
    try:
        res = run_until_stable(req.word)
        return SimulateResponse(
            generations=res.generations,
            score=res.score,
            termination_reason=res.termination_reason,
            period=res.period,
            final_live_cells=res.final_live_cells,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
