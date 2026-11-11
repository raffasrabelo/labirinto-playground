"""Testes do Q-Learning (rodam sem Pygame): python -m pytest -q"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from algorithms.base import DONE, FAIL, PATH  # noqa: E402
from algorithms.dijkstra import dijkstra  # noqa: E402
from algorithms.qlearning import AGENT, EPISODE, qlearning  # noqa: E402
from core.grid import WALL, Grid  # noqa: E402
from core.maze import generate_maze  # noqa: E402


def final(events):
    return next(e for e in reversed(events) if e.kind in (DONE, FAIL))


def optimal_cost(grid):
    return next(e for e in dijkstra(grid) if e.kind == DONE).data["cost"]


def test_aprende_o_caminho_otimo_com_os_valores_padrao():
    for size in (11, 21):
        for seed in (1, 2, 3):
            grid = generate_maze(size, size, seed, 0.10, 0.15)
            end = final(list(qlearning(grid, seed=seed)))
            assert end.kind == DONE
            assert end.data["cost"] == optimal_cost(grid)


def test_gama_baixo_deixa_o_agente_miope_em_labirinto_grande():
    # caso usado em aula: com gama 0,95 a recompensa do objetivo "some" no desconto
    grid = generate_maze(21, 21, 1, 0.10, 0.15)
    end = final(list(qlearning(grid, gamma=0.95, seed=1)))
    assert end.kind == FAIL or end.data["cost"] > optimal_cost(grid)


def test_eventos_de_episodio_e_reprodutibilidade():
    grid = generate_maze(11, 11, 7, 0.10, 0.15)
    a = list(qlearning(grid, episodes=30, seed=5))
    b = list(qlearning(grid, episodes=30, seed=5))
    assert [(e.kind, e.cell) for e in a] == [(e.kind, e.cell) for e in b]
    eps = [e for e in a if e.kind == EPISODE]
    assert len(eps) == 30 and eps[-1].data["episode"] == 30
    assert eps[1].data["epsilon"] < eps[0].data["epsilon"]  # epsilon decai
    assert all(e.cell is not None for e in a if e.kind == AGENT)


def test_sem_caminho_a_politica_falha():
    grid = Grid(7, 7)
    for y in range(7):
        grid.set((3, y), WALL)
    end = final(list(qlearning(grid, episodes=20)))
    assert end.kind == FAIL
    assert not any(e.kind == PATH for e in qlearning(grid, episodes=5))
