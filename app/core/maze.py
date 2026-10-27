"""Geração procedural de labirintos (busca em profundidade randomizada).

As "salas" ficam nas coordenadas pares e as paredes entre elas nas posições
intermediárias. Com dimensões ímpares, o labirinto ocupa a grade inteira e o
início (0, 0) e o objetivo (cols-1, rows-1) são sempre salas.
"""
from __future__ import annotations

import random

from .grid import EMPTY, MUD, WALL, Grid


def generate_maze(cols: int, rows: int, seed: int,
                  openness: float = 0.0, mud: float = 0.0) -> Grid:
    """Cria um labirinto reproduzível.

    seed      -- mesma semente => mesmo labirinto (importante para comparar
                 algoritmos e para documentar experimentos).
    openness  -- probabilidade (0..1) de remover cada parede interna, criando
                 ciclos e, portanto, caminhos alternativos.
    mud       -- probabilidade (0..1) de uma célula livre virar lama (custo 5).
    """
    # Geradores separados: alterar um parâmetro não embaralha os demais.
    rng_maze = random.Random(seed)
    rng_open = random.Random(seed + 10_000)
    rng_mud = random.Random(seed + 20_000)

    grid = Grid(cols, rows)
    grid.cells = [[WALL] * cols for _ in range(rows)]

    start = (0, 0)
    grid.cells[0][0] = EMPTY
    stack = [start]
    seen = {start}
    while stack:
        x, y = stack[-1]
        options = [(x + dx, y + dy) for dx, dy in ((0, -2), (2, 0), (0, 2), (-2, 0))
                   if 0 <= x + dx < cols and 0 <= y + dy < rows
                   and (x + dx, y + dy) not in seen]
        if not options:
            stack.pop()
            continue
        nx, ny = rng_maze.choice(options)
        grid.cells[(y + ny) // 2][(x + nx) // 2] = EMPTY  # derruba a parede
        grid.cells[ny][nx] = EMPTY
        seen.add((nx, ny))
        stack.append((nx, ny))

    for y in range(rows):
        for x in range(cols):
            is_inner_wall = grid.cells[y][x] == WALL and (x % 2) != (y % 2)
            if is_inner_wall and rng_open.random() < openness:
                grid.cells[y][x] = EMPTY

    for y in range(rows):
        for x in range(cols):
            cell = (x, y)
            if grid.cells[y][x] == EMPTY and cell not in (grid.start, grid.goal) \
                    and rng_mud.random() < mud:
                grid.cells[y][x] = MUD

    return grid
