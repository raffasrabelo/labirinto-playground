"""Q-Learning tabular: um agente aprende, por tentativa e erro, a sair do labirinto.

- Estado: a célula onde o agente está. Ações: cima, direita, baixo, esquerda.
- Recompensas: entrar numa célula custa o mesmo que nos outros algoritmos (livre -1,
  lama -5); bater na parede vale -penalidade e o agente fica no lugar; chegar ao
  objetivo vale +recompensa e encerra o episódio.
- Atualização: Q(s,a) <- Q(s,a) + alfa * [r + gama * max Q(s',.) - Q(s,a)]
- Exploração: epsilon-greedy, com epsilon multiplicado por `decay` a cada episódio.

Como os demais algoritmos, é um gerador de eventos: cada passo do agente vira um
evento AGENT, e cada fim de episódio um evento EPISODE. Depois do treino, o agente
percorre o labirinto seguindo a política aprendida (sempre a ação de maior Q) e
esse percurso é emitido como PATH.
"""
from __future__ import annotations

import random

from .base import DONE, FAIL, PATH, Event

AGENT = "agent"      # o agente fez um passo (cell = nova posição)
EPISODE = "episode"  # terminou um episódio (data: recompensa, passos, epsilon...)

ACTIONS = ((0, -1), (1, 0), (0, 1), (-1, 0))  # cima, direita, baixo, esquerda
MIN_EPSILON = 0.01


def max_steps_for(grid) -> int:
    """Limite de passos por episódio, proporcional ao número de células livres."""
    free = sum(1 for y in range(grid.rows) for x in range(grid.cols) if grid.passable((x, y)))
    return max(200, 4 * free)


def best_action(qs: list) -> int:
    """Ação de maior valor; empates resolvidos pela ordem fixa das ações."""
    best = 0
    for a in range(1, 4):
        if qs[a] > qs[best]:
            best = a
    return best


def qlearning(grid, alpha=0.5, gamma=0.995, epsilon=0.3, decay=0.99, episodes=200,
              goal_reward=100, wall_penalty=10, seed=0):
    rng = random.Random(seed)
    q: dict = {}
    start, goal = grid.start, grid.goal
    limit = max_steps_for(grid)

    def values(cell):
        qs = q.get(cell)
        if qs is None:
            qs = q[cell] = [0.0, 0.0, 0.0, 0.0]
        return qs

    def step(cell, a):
        """Ambiente: devolve (nova célula, recompensa, terminou?)."""
        dx, dy = ACTIONS[a]
        nxt = (cell[0] + dx, cell[1] + dy)
        if not grid.passable(nxt):
            return cell, -wall_penalty, False
        if nxt == goal:
            return nxt, goal_reward, True
        return nxt, -grid.cost(nxt), False

    eps = epsilon
    for episode in range(1, episodes + 1):
        cell, total, steps, reached = start, 0.0, 0, False
        yield Event(AGENT, cell, {"q": q, "episode": episode, "epsilon": eps, "new_episode": True})
        while steps < limit:
            qs = values(cell)
            a = rng.randrange(4) if rng.random() < eps else best_action(qs)
            nxt, r, done = step(cell, a)
            target = r if done else r + gamma * max(values(nxt))
            qs[a] += alpha * (target - qs[a])
            cell = nxt
            total += r
            steps += 1
            yield Event(AGENT, cell)
            if done:
                reached = True
                break
        yield Event(EPISODE, data={"episode": episode, "episodes": episodes, "reward": total,
                                   "steps": steps, "reached": reached, "epsilon": eps})
        eps = max(MIN_EPSILON, eps * decay)

    # política aprendida: segue sempre a melhor ação, sem explorar
    path, cell, seen = [start], start, {start}
    while cell != goal and len(path) <= limit:
        nxt, _, _ = step(cell, best_action(values(cell)))
        if nxt in seen:          # ficou em ciclo ou bateu na parede: política incompleta
            break
        path.append(nxt)
        seen.add(nxt)
        cell = nxt
    if cell != goal:
        yield Event(FAIL, data={"reason": "policy"})
        return
    for c in path:
        yield Event(PATH, c)
    yield Event(DONE, data={"cost": grid.path_cost(path), "moves": len(path) - 1})
