"""Modelo da grade do labirinto.

Este módulo NÃO depende do Pygame: ele descreve apenas o "mundo" (células,
paredes, custos, início e objetivo). Assim os algoritmos podem ser testados
com pytest e reutilizados por qualquer interface.
"""
from __future__ import annotations

EMPTY, WALL, MUD = 0, 1, 2

# Custo para ENTRAR em uma célula. Paredes não são atravessáveis.
CELL_COST = {EMPTY: 1, MUD: 5}

# Ordem fixa de vizinhos: cima, direita, baixo, esquerda.
DIRECTIONS = ((0, -1), (1, 0), (0, 1), (-1, 0))

Cell = tuple  # (coluna, linha)


class Grid:
    def __init__(self, cols: int, rows: int):
        self.cols = cols
        self.rows = rows
        self.cells = [[EMPTY] * cols for _ in range(rows)]
        self.start: Cell = (0, 0)
        self.goal: Cell = (cols - 1, rows - 1)

    def in_bounds(self, cell: Cell) -> bool:
        x, y = cell
        return 0 <= x < self.cols and 0 <= y < self.rows

    def get(self, cell: Cell) -> int:
        x, y = cell
        return self.cells[y][x]

    def set(self, cell: Cell, kind: int) -> None:
        """Altera uma célula. Início e objetivo nunca viram parede."""
        if kind == WALL and cell in (self.start, self.goal):
            return
        x, y = cell
        self.cells[y][x] = kind

    def fill(self, kind: int) -> None:
        for y in range(self.rows):
            for x in range(self.cols):
                self.set((x, y), kind)

    def passable(self, cell: Cell) -> bool:
        return self.in_bounds(cell) and self.get(cell) != WALL

    def cost(self, cell: Cell) -> int:
        return CELL_COST[self.get(cell)]

    def neighbors(self, cell: Cell) -> list:
        """Vizinhos atravessáveis (4 direções)."""
        x, y = cell
        result = []
        for dx, dy in DIRECTIONS:
            n = (x + dx, y + dy)
            if self.passable(n):
                result.append(n)
        return result

    def path_cost(self, path: list) -> int:
        """Custo total de um caminho (a célula inicial não é cobrada)."""
        return sum(self.cost(c) for c in path[1:])

    def move_endpoint(self, which: str, cell: Cell) -> None:
        """Move o início ('start') ou o objetivo ('goal') para `cell`."""
        other = self.goal if which == "start" else self.start
        if not self.in_bounds(cell) or cell == other:
            return
        if self.get(cell) == WALL:
            x, y = cell
            self.cells[y][x] = EMPTY
        setattr(self, which, cell)
