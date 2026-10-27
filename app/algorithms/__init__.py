"""Registro dos algoritmos disponíveis na plataforma.

Para adicionar um algoritmo novo basta criar o gerador e registrá-lo aqui.
"""
from dataclasses import dataclass

from .backtracking import backtracking
from .dijkstra import dijkstra


@dataclass(frozen=True)
class AlgorithmInfo:
    name: str
    run: object          # função geradora (grid) -> Event, ou None
    description: str
    available: bool = True


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
        None,
        "Previsto para a Sprint 3: um agente aprende por tentativa e erro, "
        "recebendo recompensas, com parâmetros alfa (aprendizado), gama "
        "(desconto) e épsilon (exploração).",
        available=False,
    ),
}
