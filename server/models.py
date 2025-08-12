from typing import Optional
from pydantic import BaseModel, Field

class SimulateRequest(BaseModel):
    word: str = Field(..., min_length=1, description="ASCII word to seed the grid")

class SimulateResponse(BaseModel):
    generations: int
    score: int
    termination_reason: str
    period: Optional[int] = None
    final_live_cells: int
