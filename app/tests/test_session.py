"""Testes da sessão (comandos vindos da interface HTML), sem Pygame."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.grid import MUD, WALL  # noqa: E402
from core.session import FINISHED, IDLE, PAUSED, RUNNING, Session  # noqa: E402


def run_to_end(s):
    while s.mode != FINISHED:
        s.update(1.0)
    return s.snapshot()


def test_parametros_sao_validados():
    s = Session()
    s.command({"type": "set", "name": "size", "value": 999})
    assert s.params["size"] == 61 and s.grid.cols == 61
    s.command({"type": "set", "name": "size", "value": 20})
    assert s.params["size"] == 21  # força ímpar
    s.command({"type": "set", "name": "speed", "value": "0"})
    assert s.params["speed"] == 1
    s.command({"type": "set", "name": "algorithm", "value": "inexistente"})
    assert s.params["algorithm"] == "dijkstra"
    s.command({"type": "set", "name": "alpha", "value": "7"})
    assert s.params["alpha"] == 1.0
    s.command({"type": "set", "name": "gamma", "value": 0.95})
    assert s.params["gamma"] == 0.95
    s.command({"type": "set", "name": "episodes", "value": 3})
    assert s.params["episodes"] == 10
    s.command({"type": "set", "name": "inexistente", "value": 1})
    s.command({"type": "set", "name": "brush", "value": "fogo"})
    assert s.params["brush"] == "wall"


def test_ciclo_de_execucao():
    s = Session()
    assert s.mode == IDLE
    s.command({"type": "step"})
    assert s.mode == PAUSED and s.run.steps == 1
    s.command({"type": "play"})
    assert s.mode == RUNNING
    s.command({"type": "play"})
    assert s.mode == PAUSED
    s.command({"type": "set", "name": "speed", "value": 1000})
    s.command({"type": "play"})
    snap = run_to_end(s)
    assert snap["status"] == "found"
    assert snap["metrics"]["cost"] == 120 and snap["metrics"]["moves"] == 56
    s.command({"type": "reset"})
    assert s.mode == IDLE and s.snapshot()["metrics"]["steps"] == 0


def test_mesmos_resultados_da_demo():
    s = Session()
    s.command({"type": "set", "name": "algorithm", "value": "backtracking"})
    s.command({"type": "set", "name": "speed", "value": 1000})
    s.command({"type": "play"})
    m = run_to_end(s)["metrics"]
    assert (m["cost"], m["moves"], m["visited"]) == (132, 64, 71)


def test_mudar_parametro_do_labirinto_regenera_e_reinicia():
    s = Session()
    s.command({"type": "play"})
    s.update(0.5)
    version = s.maze_version
    s.command({"type": "set", "name": "mud", "value": 0})
    assert s.maze_version == version + 1 and s.mode == IDLE
    assert all(s.grid.get((x, y)) != MUD for y in range(s.grid.rows) for x in range(s.grid.cols))


def test_edicao_com_mouse():
    s = Session()
    s.command({"type": "set", "name": "openness", "value": 50})
    free = next((x, y) for y in range(s.grid.rows) for x in range(s.grid.cols)
                if s.grid.get((x, y)) == 0 and (x, y) not in (s.grid.start, s.grid.goal))
    s.edit_begin(free)
    s.edit_end()
    assert s.grid.get(free) == WALL
    s.edit_begin(free, erase=True)
    s.edit_end()
    assert s.grid.get(free) == 0
    s.edit_begin(s.grid.start)
    s.edit_drag((2, 0))
    s.edit_end()
    assert s.grid.start == (2, 0)


def test_retrato_e_serializavel_em_json():
    import json
    s = Session()
    s.command({"type": "step"})
    data = json.loads(json.dumps(s.snapshot()))
    assert set(data) >= {"mode", "status", "params", "metrics", "description"}


def test_q_learning_pela_sessao_aprende_o_caminho_otimo():
    s = Session()                                   # 21x21, semente 42 (padrão da demo)
    s.command({"type": "set", "name": "algorithm", "value": "qlearning"})
    s.command({"type": "set", "name": "speed", "value": 100_000})
    s.command({"type": "play"})
    snap = run_to_end(s)
    m = snap["metrics"]
    assert snap["status"] == "found"
    assert m["cost"] == 120                          # o mesmo custo ótimo do Dijkstra
    assert m["episode"] == 200 and m["reached"] > 150
    assert 0 < len(snap["rewards"]) <= 200
    assert snap["rewards"][-1] > snap["rewards"][0]  # a recompensa melhora com o treino


def test_mudar_parametro_do_q_learning_reinicia_o_treino():
    s = Session()
    s.command({"type": "set", "name": "algorithm", "value": "qlearning"})
    s.command({"type": "play"})
    s.update(0.5)
    assert s.mode == RUNNING
    s.command({"type": "set", "name": "gamma", "value": 0.9})
    assert s.mode == IDLE and s.run.steps == 0
