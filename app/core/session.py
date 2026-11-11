"""Sessão do playground: parâmetros, labirinto e execução.

Não depende do Pygame nem do navegador. A interface (HTML no navegador ou
teclado no desktop) envia COMANDOS em forma de dicionário e lê de volta um
RETRATO (snapshot) do estado. Assim a mesma lógica serve às duas versões e
pode ser testada com pytest.
"""
from __future__ import annotations

import random
import time

from algorithms import ALGORITHMS
from algorithms.base import DONE, FAIL

from .grid import EMPTY, MUD, WALL
from .maze import generate_maze
from .run_state import RunState

IDLE, RUNNING, PAUSED, FINISHED = "idle", "running", "paused", "finished"

BRUSHES = {"wall": WALL, "mud": MUD, "erase": EMPTY}

# nome do parâmetro -> (mínimo, máximo)
LIMITS = {
    "size": (11, 61),
    "openness": (0, 50),
    "mud": (0, 40),
    "seed": (1, 999),
    "speed": (1, 100_000),
    # Q-Learning
    "episodes": (10, 5000),
    "goal_reward": (1, 1000),
    "wall_penalty": (0, 100),
}
FLOAT_LIMITS = {
    "alpha": (0.01, 1.0),
    "gamma": (0.0, 0.999),
    "epsilon": (0.0, 1.0),
    "decay": (0.9, 1.0),
}
MAZE_PARAMS = {"size", "openness", "mud", "seed"}
QL_PARAMS = {"alpha", "gamma", "epsilon", "decay", "episodes", "goal_reward", "wall_penalty"}
FRAME_BUDGET = 0.012   # segundos de processamento por quadro (mantém a página fluida)
CHART_POINTS = 200     # pontos máximos do gráfico de recompensa


class Session:
    def __init__(self):
        self.params = {
            "algorithm": "dijkstra",
            "size": 21,
            "openness": 10,
            "mud": 15,
            "seed": 42,
            "speed": 20,
            "brush": "wall",
            "show_numbers": True,
            # Q-Learning (valores escolhidos por experimento: ver docs/06-algoritmos.md)
            "alpha": 0.5,
            "gamma": 0.995,
            "epsilon": 0.3,
            "decay": 0.99,
            "episodes": 200,
            "goal_reward": 100,
            "wall_penalty": 10,
            "show_policy": True,
        }
        self.maze_version = 0    # muda sempre que o labirinto muda
        self.drag = None         # "start" | "goal" | tipo de célula sendo pintado
        self.regenerate()

    # ------------------------------------------------------------ comandos --
    def command(self, cmd: dict) -> None:
        kind = cmd.get("type")
        if kind == "set":
            self.set_param(cmd["name"], cmd["value"])
        elif kind == "play":
            self.toggle_play()
        elif kind == "step":
            self.step()
        elif kind == "reset":
            self.reset_run()
        elif kind == "new_maze":
            self.new_maze()
        elif kind == "clear":
            self.clear_grid()

    def set_param(self, name: str, value) -> None:
        if name in LIMITS:
            low, high = LIMITS[name]
            value = max(low, min(high, int(value)))
            if name == "size" and value % 2 == 0:
                value += 1  # o gerador exige dimensões ímpares
        elif name in FLOAT_LIMITS:
            low, high = FLOAT_LIMITS[name]
            value = round(max(low, min(high, float(value))), 3)
        elif name == "algorithm":
            info = ALGORITHMS.get(value)
            if info is None or not info.available:
                return
        elif name == "brush":
            if value not in BRUSHES:
                return
        elif name in ("show_numbers", "show_policy"):
            value = bool(value)
        else:
            return

        if self.params[name] == value:
            return
        self.params[name] = value
        if name in MAZE_PARAMS:
            self.regenerate()
        elif name == "algorithm" or (name in QL_PARAMS and self.params["algorithm"] == "qlearning"):
            self.reset_run()

    def regenerate(self) -> None:
        p = self.params
        self.grid = generate_maze(p["size"], p["size"], p["seed"], p["openness"] / 100, p["mud"] / 100)
        self.maze_version += 1
        self.reset_run()

    def new_maze(self) -> None:
        low, high = LIMITS["seed"]
        self.params["seed"] = random.randint(low, high)
        self.regenerate()

    def clear_grid(self) -> None:
        self.grid.fill(EMPTY)
        self.maze_version += 1
        self.reset_run()

    def reset_run(self) -> None:
        self.mode, self.gen, self.run, self.accum = IDLE, None, RunState(), 0.0

    def _start(self) -> None:
        self.run = RunState()
        info = ALGORITHMS[self.params["algorithm"]]
        kwargs = {name: self.params[name] for name in info.params}
        self.gen = info.run(self.grid, **kwargs)
        self.accum = 0.0

    def toggle_play(self) -> None:
        if self.mode in (IDLE, FINISHED):
            self._start()
            self.mode = RUNNING
        elif self.mode == RUNNING:
            self.mode = PAUSED
        else:
            self.mode = RUNNING

    def step(self) -> None:
        if self.mode == FINISHED:
            return
        if self.mode == IDLE:
            self._start()
        self.mode = PAUSED
        self._advance()

    def _advance(self) -> bool:
        """Consome um evento do algoritmo. Retorna False quando terminou."""
        try:
            ev = next(self.gen)
        except StopIteration:
            self.mode = FINISHED
            return False
        self.run.apply(ev)
        if ev.kind in (DONE, FAIL):
            self.mode = FINISHED
            return False
        return True

    def update(self, dt: float) -> None:
        if self.mode != RUNNING:
            return
        self.accum += dt * self.params["speed"]
        n = int(self.accum)
        self.accum -= n
        deadline = time.perf_counter() + FRAME_BUDGET
        for i in range(n):
            if not self._advance():
                break
            # em velocidades altas, para no limite de tempo do quadro e descarta o
            # atraso acumulado (senão a página trava tentando "alcançar")
            if i % 64 == 63 and time.perf_counter() > deadline:
                self.accum = 0.0
                break

    # ------------------------------------------------- edição com o mouse --
    def edit_begin(self, cell, erase: bool = False) -> None:
        if cell is None:
            return
        if erase:
            self.drag = EMPTY
        elif cell == self.grid.start:
            self.drag = "start"
        elif cell == self.grid.goal:
            self.drag = "goal"
        else:
            self.drag = BRUSHES[self.params["brush"]]
        self.edit_drag(cell)

    def edit_drag(self, cell) -> None:
        if cell is None or self.drag is None:
            return
        if self.drag in ("start", "goal"):
            self.grid.move_endpoint(self.drag, cell)
        else:
            self.grid.set(cell, self.drag)
        self.maze_version += 1
        self.reset_run()

    def edit_end(self) -> None:
        self.drag = None

    # ------------------------------------------------------------- retrato --
    def snapshot(self) -> dict:
        run = self.run
        if self.mode == FINISHED:
            status = "found" if run.found else "no_path"
        else:
            status = self.mode
        info = ALGORITHMS[self.params["algorithm"]]
        return {
            "mode": self.mode,
            "status": status,
            "params": dict(self.params),
            "description": info.description,
            "metrics": {
                "steps": run.steps,
                "visited": run.visited,
                "frontier": run.counts["frontier"],
                "depth": run.depth,
                "max_depth": run.max_depth,
                "moves": run.result.get("moves"),
                "cost": run.result.get("cost"),
                # Q-Learning
                "episode": run.episode,
                "episodes": self.params["episodes"],
                "epsilon": None if run.epsilon is None else round(run.epsilon, 3),
                "episode_steps": run.episode_steps,
                "last_reward": round(run.rewards[-1], 1) if run.rewards else None,
                "reached": run.reached,
            },
            "rewards": downsample(run.rewards, CHART_POINTS),
        }


def downsample(values: list, points: int) -> list:
    """Reduz a série a no máximo `points` médias de blocos (para o gráfico)."""
    if len(values) <= points:
        return [round(v, 1) for v in values]
    size = len(values) / points
    out = []
    for i in range(points):
        block = values[int(i * size):int((i + 1) * size)] or values[-1:]
        out.append(round(sum(block) / len(block), 1))
    return out
