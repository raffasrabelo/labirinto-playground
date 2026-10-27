"""Testes da lógica (rodam sem Pygame): python -m pytest -q"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from algorithms.backtracking import backtracking  # noqa: E402
from algorithms.base import DONE, FAIL, PATH  # noqa: E402
from algorithms.dijkstra import dijkstra  # noqa: E402
from core.grid import EMPTY, MUD, WALL, Grid  # noqa: E402
from core.maze import generate_maze  # noqa: E402
from core.run_state import RunState  # noqa: E402


def run(algorithm, grid):
    state = RunState()
    for ev in algorithm(grid):
        state.apply(ev)
    return state


def assert_valid_path(grid, path):
    assert path[0] == grid.start and path[-1] == grid.goal
    for a, b in zip(path, path[1:]):
        assert abs(a[0] - b[0]) + abs(a[1] - b[1]) == 1
        assert grid.passable(b)


def test_dijkstra_desvia_da_lama():
    #  I .      atravessar a lama custa 5 + 1 = 6;
    #  ~ .      contornar pela direita custa 1 + 1 + 1 + 1 = 4.
    #  O .
    grid = Grid(2, 3)
    grid.goal = (0, 2)
    grid.set((0, 1), MUD)
    state = run(dijkstra, grid)
    assert state.found
    assert state.result["cost"] == 4
    assert state.result["moves"] == 4
    assert_valid_path(grid, state.path)


def test_dijkstra_e_otimo_em_labirintos_aleatorios():
    for seed in range(20):
        grid = generate_maze(15, 15, seed, openness=0.3, mud=0.3)
        dij = run(dijkstra, grid)
        bt = run(backtracking, grid)
        assert dij.found and bt.found
        assert_valid_path(grid, dij.path)
        assert dij.result["cost"] == grid.path_cost(dij.path)
        assert dij.result["cost"] <= bt.result["cost"]


def test_backtracking_encontra_caminho_valido():
    grid = generate_maze(21, 21, seed=7)
    state = run(backtracking, grid)
    assert state.found
    assert_valid_path(grid, state.path)
    assert state.max_depth >= len(state.path)


def test_sem_caminho():
    grid = Grid(5, 5)
    for y in range(5):
        grid.set((2, y), WALL)
    for algorithm in (dijkstra, backtracking):
        state = run(algorithm, grid)
        assert state.finished and not state.found
        assert state.counts["path"] == 0


def test_labirinto_perfeito_e_conexo_e_reproduzivel():
    a = generate_maze(21, 21, seed=123)
    b = generate_maze(21, 21, seed=123)
    assert a.cells == b.cells
    # Todas as células livres devem ser alcançáveis a partir do início.
    free = {(x, y) for y in range(21) for x in range(21) if a.get((x, y)) == EMPTY}
    seen, todo = {a.start}, [a.start]
    while todo:
        for n in a.neighbors(todo.pop()):
            if n not in seen:
                seen.add(n)
                todo.append(n)
    assert free <= seen


def test_eventos_terminam_com_done_ou_fail():
    grid = generate_maze(11, 11, seed=1)
    for algorithm in (dijkstra, backtracking):
        events = list(algorithm(grid))
        assert events[-1].kind in (DONE, FAIL)
        assert any(e.kind == PATH for e in events)
