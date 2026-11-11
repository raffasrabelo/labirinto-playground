"""Registro dos algoritmos disponíveis na plataforma.

Para adicionar um algoritmo novo basta criar o gerador e registrá-lo aqui.
`params` lista os parâmetros da sessão repassados ao gerador.
"""
from dataclasses import dataclass

from .backtracking import backtracking
from .dijkstra import dijkstra
from .qlearning import qlearning


@dataclass(frozen=True)
class AlgorithmInfo:
    name: str
    run: object          # função geradora (grid, **params) -> Event
    description: str
    available: bool = True
    params: tuple = ()


ALGORITHMS = {
    "backtracking": AlgorithmInfo(
        "Backtracking",
        backtracking,
        "Busca em profundidade recursiva: avança para o primeiro vizinho livre "
        "ainda não visitado e, ao chegar em um beco sem saída, RETROCEDE "
        "(desempilha) até a última bifurcação com alternativas. Encontra UM "
        "caminho, mas não garante o de menor custo. Compare o custo com o "
        "Dijkstra no mesmo labirinto (mesma semente).",
    ),
    "dijkstra": AlgorithmInfo(
        "Dijkstra",
        dijkstra,
        "Expande sempre a célula de MENOR custo acumulado, retirada de uma fila "
        "de prioridade (heap). Lama custa 5 e as demais células custam 1, por "
        "isso o caminho final é o de menor custo, não necessariamente o de "
        "menos passos. Os números indicam a distância acumulada desde o início.",
    ),
    "qlearning": AlgorithmInfo(
        "Q-Learning",
        qlearning,
        "O agente não conhece o labirinto: aprende por tentativa e erro. A cada "
        "passo recebe uma recompensa (−1 por célula, −5 na lama, penalidade ao "
        "bater na parede, bônus ao chegar) e atualiza a tabela Q. A cor das "
        "células mostra o valor aprendido e as setas, a melhor ação em cada "
        "lugar. No fim, ele percorre o labirinto seguindo o que aprendeu. "
        "Experimente baixar o gama para 0,95 em uma grade 21 × 21.",
        params=("alpha", "gamma", "epsilon", "decay", "episodes", "goal_reward",
                "wall_penalty", "seed"),
    ),
}
