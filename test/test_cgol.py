import numpy as np
from server.cgol import word_to_seed, place_seed_center, run_until_stable, GRID_H, GRID_W

def test_word_to_seed_shapes():
    seed = word_to_seed("A")
    assert seed.shape == (1, 8)
    seed2 = word_to_seed("ABC")
    assert seed2.shape == (3, 8)

def test_place_seed_center_bounds():
    seed = np.ones((2, 8), dtype=bool)
    grid = place_seed_center(seed)
    assert grid.shape == (GRID_H, GRID_W)
    assert grid.sum() == 16

def test_run_basic_extinction():
    res = run_until_stable("A")
    assert res.generations >= 0
    assert res.score >= 0
