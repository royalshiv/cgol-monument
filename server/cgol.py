from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple, Dict, Optional
import numpy as np

GRID_W = 60
GRID_H = 40

@dataclass
class RunResult:
    generations: int
    score: int
    termination_reason: str
    period: Optional[int]
    final_live_cells: int

def word_to_seed(word: str) -> np.ndarray:
    if not word or not word.strip():
        raise ValueError("word must be a non-empty string")
    rows = []
    for ch in word:
        code = ord(ch)
        if code > 255:
            raise ValueError(f"character out of ASCII range: {ch!r}")
        bits = f"{code:08b}"
        rows.append([c == '1' for c in bits])
    return np.array(rows, dtype=bool)

def place_seed_center(seed: np.ndarray, grid_w: int = GRID_W, grid_h: int = GRID_H) -> np.ndarray:
    h, w = seed.shape
    if h > grid_h or w > grid_w:
        raise ValueError("seed larger than grid")
    grid = np.zeros((grid_h, grid_w), dtype=bool)
    top = (grid_h - h) // 2
    left = (grid_w - w) // 2
    grid[top:top+h, left:left+w] = seed
    return grid

def step(grid: np.ndarray) -> Tuple[np.ndarray, int]:
    neighbors = sum(np.roll(np.roll(grid, dy, axis=0), dx, axis=1)
                    for dy in (-1, 0, 1)
                    for dx in (-1, 0, 1)
                    if not (dx == 0 and dy == 0))
    survive = (grid & ((neighbors == 2) | (neighbors == 3)))
    born = (~grid & (neighbors == 3))
    return (survive | born), int(born.sum())

def grid_hash(grid: np.ndarray) -> bytes:
    return grid.tobytes()

def run_until_stable(word: str, max_generations: int = 1000, periodicity_cap: int = 10) -> RunResult:
    seed = word_to_seed(word)
    grid = place_seed_center(seed)
    seen: Dict[bytes, int] = {grid_hash(grid): 0}
    total_births = 0
    generations = 0

    if not grid.any():
        return RunResult(0, 0, "extinction", None, 0)

    while generations < max_generations:
        grid, births = step(grid)
        total_births += births
        generations += 1

        if not grid.any():
            return RunResult(generations, total_births, "extinction", None, 0)

        h = grid_hash(grid)
        if h in seen:
            period = generations - seen[h]
            if period == 1:
                return RunResult(generations, total_births, "static", 1, int(grid.sum()))
            if period < periodicity_cap:
                return RunResult(generations, total_births, "periodic", period, int(grid.sum()))
        else:
            seen[h] = generations

    return RunResult(generations, total_births, "max_generations", None, int(grid.sum()))
