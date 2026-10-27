"""Contrato comum a todos os algoritmos da plataforma.

Cada algoritmo é um GERADOR Python: a cada `yield` ele devolve um Event
descrevendo o que acabou de fazer. A interface consome N eventos por segundo
(controle de velocidade), o que torna possível pausar e executar passo a
passo sem que o algoritmo saiba nada sobre desenho.
"""
from __future__ import annotations

from dataclasses import dataclass, field

FRONTIER = "frontier"    # célula descoberta / entrou na fila
VISIT = "visit"          # célula expandida (processada)
BACKTRACK = "backtrack"  # célula abandonada (retrocesso)
PATH = "path"            # célula pertence ao caminho final
DONE = "done"            # objetivo alcançado
FAIL = "fail"            # não existe caminho


@dataclass(frozen=True)
class Event:
    kind: str
    cell: tuple = None
    data: dict = field(default_factory=dict)
