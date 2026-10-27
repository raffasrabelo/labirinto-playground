"""Backtracking: busca em profundidade com retrocesso.

A recursão é simulada com uma pilha explícita, que é exatamente a "pilha de
chamadas" da versão recursiva. Isso evita o limite de recursão do Python em
labirintos grandes e permite mostrar a profundidade da pilha na interface.

Versão recursiva equivalente (para o texto do TCC):

    def resolver(celula):
        if celula == objetivo: return True
        marcar(celula)
        for vizinho in vizinhos(celula):
            if not marcado(vizinho) and resolver(vizinho):
                return True
        return False          # <- retrocesso
"""
from __future__ import annotations

from .base import BACKTRACK, DONE, FAIL, PATH, VISIT, Event


def backtracking(grid):
    start, goal = grid.start, grid.goal
    visited = {start}
    stack = [(start, iter(grid.neighbors(start)))]
    yield Event(VISIT, start, {"depth": 1})

    while stack:
        cell, options = stack[-1]
        if cell == goal:
            path = [c for c, _ in stack]
            for c in path:
                yield Event(PATH, c)
            yield Event(DONE, data={"cost": grid.path_cost(path), "moves": len(path) - 1})
            return

        for n in options:
            if n not in visited:
                visited.add(n)
                stack.append((n, iter(grid.neighbors(n))))
                yield Event(VISIT, n, {"depth": len(stack)})
                break
        else:  # nenhuma alternativa restante: beco sem saída
            stack.pop()
            top = stack[-1][0] if stack else None
            yield Event(BACKTRACK, cell, {"depth": len(stack), "to": top})

    yield Event(FAIL)
