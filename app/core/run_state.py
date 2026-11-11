"""Estado visual de uma execução.

Os algoritmos emitem eventos (algorithms/base.py); o RunState os acumula em
um "retrato" que a interface apenas desenha. Separar isso permite pausar,
avançar passo a passo e testar a visualização sem abrir janela.
"""
from __future__ import annotations

from collections import Counter

from algorithms.base import BACKTRACK, DONE, FAIL, FRONTIER, PATH, VISIT, Event
from algorithms.qlearning import AGENT, EPISODE

FRONTIER_STATE, VISITED_STATE, DEAD_STATE, PATH_STATE = "frontier", "visited", "dead", "path"


class RunState:
    def __init__(self):
        self.cells: dict = {}      # célula -> estado visual
        self.dist: dict = {}       # célula -> custo acumulado (Dijkstra)
        self.counts = Counter()    # estado -> quantidade de células
        self.current = None        # célula sendo processada agora
        self.steps = 0
        self.visited = 0
        self.depth = 0             # tamanho atual da pilha (Backtracking)
        self.max_depth = 0
        self.path: list = []
        self.finished = False
        self.found = False
        self.result: dict = {}
        # Q-Learning
        self.q = None              # tabela Q (referência viva, só leitura)
        self.episode = 0
        self.episodes = 0
        self.epsilon = None
        self.episode_steps = 0
        self.rewards: list = []    # recompensa total de cada episódio
        self.reached = 0           # episódios que chegaram ao objetivo

    def _set(self, cell, state: str) -> None:
        old = self.cells.get(cell)
        if old:
            self.counts[old] -= 1
        self.cells[cell] = state
        self.counts[state] += 1

    def apply(self, ev: Event) -> None:
        self.steps += 1
        kind = ev.kind
        if kind == AGENT:                         # o mais frequente, por isso primeiro
            self.current = ev.cell
            if ev.data:
                self.q = ev.data["q"]
                self.episode = ev.data["episode"]
                self.epsilon = ev.data["epsilon"]
                self.episode_steps = 0
            else:
                self.episode_steps += 1
        elif kind == EPISODE:
            self.rewards.append(ev.data["reward"])
            self.episodes = ev.data["episodes"]
            self.reached += ev.data["reached"]
        elif kind == FRONTIER:
            if self.cells.get(ev.cell) != VISITED_STATE:
                self._set(ev.cell, FRONTIER_STATE)
            self.dist[ev.cell] = ev.data["dist"]
        elif kind == VISIT:
            self._set(ev.cell, VISITED_STATE)
            self.visited += 1
            self.current = ev.cell
            if "depth" in ev.data:
                self.depth = ev.data["depth"]
                self.max_depth = max(self.max_depth, self.depth)
        elif kind == BACKTRACK:
            self._set(ev.cell, DEAD_STATE)
            self.depth = ev.data["depth"]
            self.current = ev.data.get("to")
        elif kind == PATH:
            self._set(ev.cell, PATH_STATE)
            self.path.append(ev.cell)
        elif kind in (DONE, FAIL):
            self.finished = True
            self.found = kind == DONE
            self.result = dict(ev.data)
            self.current = None
