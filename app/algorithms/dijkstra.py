"""Dijkstra: menor custo da origem ao objetivo usando fila de prioridade."""
from __future__ import annotations

import heapq
from itertools import count

from .base import DONE, FAIL, FRONTIER, PATH, VISIT, Event


def dijkstra(grid):
    start, goal = grid.start, grid.goal
    dist = {start: 0}
    prev = {}
    visited = set()
    tie = count()  # desempate estável na heap
    heap = [(0, next(tie), start)]
    yield Event(FRONTIER, start, {"dist": 0})

    while heap:
        d, _, cell = heapq.heappop(heap)
        if cell in visited:
            continue  # entrada antiga na heap (já achamos distância menor)
        visited.add(cell)
        yield Event(VISIT, cell, {"dist": d, "queue": len(heap)})

        if cell == goal:
            path = [cell]
            while path[-1] != start:
                path.append(prev[path[-1]])
            path.reverse()
            for c in path:
                yield Event(PATH, c)
            yield Event(DONE, data={"cost": d, "moves": len(path) - 1})
            return

        for n in grid.neighbors(cell):
            if n in visited:
                continue
            nd = d + grid.cost(n)
            if nd < dist.get(n, float("inf")):  # relaxamento da aresta
                dist[n] = nd
                prev[n] = cell
                heapq.heappush(heap, (nd, next(tie), n))
                yield Event(FRONTIER, n, {"dist": nd})

    yield Event(FAIL)
