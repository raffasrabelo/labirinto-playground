# 02 · Arquitetura e Fluxos da Plataforma

## Tecnologias

| Camada | Tecnologia | Por quê |
|---|---|---|
| Linguagem | Python 3.12+ | Definida no TCC; sintaxe próxima do pseudocódigo das disciplinas |
| Gráficos e interação | **pygame-ce** (Community Edition do Pygame) | É a versão que o pygbag usa no navegador; API compatível com o Pygame |
| Web | **pygbag** (Pygame → WebAssembly) | Roda o mesmo código Python no navegador, sem instalação |
| Testes | pytest | Valida a lógica dos algoritmos sem abrir janela |
| Hospedagem | GitHub Pages (ou itch.io) | Gratuita e com link público para os stakeholders |
| Versionamento | Git + GitHub | Histórico por sprint (tags `sprint-N`) |

## Decisão central: algoritmos como **geradores de eventos**

Cada algoritmo é uma função geradora Python que, a cada `yield`, devolve um `Event`
(`frontier`, `visit`, `backtrack`, `path`, `done`, `fail`). O algoritmo **não sabe
desenhar**; a interface **não sabe resolver labirintos**.

Isso traz quatro ganhos, todos citáveis no TCC:
1. **Passo a passo de graça:** pausar é parar de chamar `next()`.
2. **Velocidade ajustável:** a interface consome N eventos por segundo.
3. **Testabilidade:** os testes executam o gerador até o fim e conferem o resultado (RNF03).
4. **Extensibilidade:** um algoritmo novo é só mais um gerador registrado em `algorithms/__init__.py`.

## Visão em camadas

```mermaid
flowchart TB
    subgraph Navegador["Navegador (WebAssembly via pygbag) / Desktop"]
        subgraph UI["ui/ - Apresentação (Pygame)"]
            PG["playground.py<br/>controlador da tela"]
            W["widgets.py<br/>botões, sliders, seletores"]
            T["theme.py<br/>cores e fontes"]
        end
        subgraph CORE["core/ - Modelo (Python puro)"]
            G["grid.py<br/>células, paredes, custos"]
            M["maze.py<br/>gerador procedural"]
            RS["run_state.py<br/>estado visual da execução"]
        end
        subgraph ALG["algorithms/ - Algoritmos (Python puro)"]
            B["base.py<br/>contrato Event"]
            D["dijkstra.py"]
            BT["backtracking.py"]
            Q["qlearning.py (S3)"]
        end
    end
    PG --> W & T
    PG --> G & M & RS
    PG -- "next(gerador)" --> D & BT & Q
    D & BT & Q -- "Event" --> RS
    D & BT & Q --> G
    TESTS["tests/ (pytest)"] -.-> CORE & ALG
```

## Estrutura de pastas

```
app/
├── main.py              # ponto de entrada (laço assíncrono exigido pelo pygbag)
├── algorithms/
│   ├── __init__.py      # registro: nome, função, descrição, disponível?
│   ├── base.py          # Event + tipos de evento
│   ├── dijkstra.py
│   └── backtracking.py
├── core/
│   ├── grid.py          # modelo do labirinto
│   ├── maze.py          # geração com semente
│   └── run_state.py     # aplica eventos -> estado desenhável
├── ui/
│   ├── playground.py    # layout, eventos de mouse/teclado, desenho
│   ├── widgets.py
│   └── theme.py
└── tests/
    └── test_algorithms.py
```

## Fluxo de uso (jornada do aluno)

```mermaid
flowchart LR
    A([Abre o link]) --> B[Escolhe o algoritmo]
    B --> C[Ajusta parâmetros<br/>tamanho, aberturas, lama, semente]
    C --> D[Edita o labirinto<br/>paredes, lama, início/objetivo]
    D --> E[Executa ou avança passo a passo]
    E --> F[Observa cores, números,<br/>métricas e explicação]
    F --> G{Entendeu?}
    G -- "não" --> H[Reduz a velocidade<br/>ou usa Passo]
    H --> E
    G -- "quer comparar" --> I[Troca o algoritmo<br/>mantendo a semente]
    I --> E
    G -- "quer testar hipótese" --> C
```

## Ciclo de execução (a cada quadro, 60×/s)

```mermaid
sequenceDiagram
    actor U as Aluno
    participant P as Playground (ui)
    participant A as Algoritmo (gerador)
    participant R as RunState (core)
    U->>P: clica "Executar"
    P->>A: cria gerador(grid)
    loop a cada quadro
        P->>P: eventos de mouse/teclado
        Note over P: n = velocidade × Δt
        loop n vezes
            P->>A: next()
            A-->>P: Event(kind, cell, data)
            P->>R: apply(event)
        end
        P->>P: desenha grade + métricas a partir do RunState
    end
    A-->>P: Event(done/fail)
    P-->>U: status "Caminho encontrado", custo, passos
```

## Estados da execução

```mermaid
stateDiagram-v2
    [*] --> Pronto
    Pronto --> Executando: Executar / Espaço
    Pronto --> Pausado: Passo / N
    Executando --> Pausado: Pausar
    Pausado --> Executando: Continuar
    Pausado --> Pausado: Passo
    Executando --> Concluído: evento done/fail
    Pausado --> Concluído: evento done/fail
    Concluído --> Executando: Executar de novo
    Executando --> Pronto: editar grade / mudar parâmetro / Reiniciar
    Pausado --> Pronto: editar grade / mudar parâmetro / Reiniciar
    Concluído --> Pronto: editar grade / mudar parâmetro / Reiniciar
```

## Modelo do labirinto

- Grade de `N × N` células com N ímpar (11 a 61). Cada célula é **livre** (custo 1), **lama** (custo 5) ou **parede**.
- Geração: busca em profundidade randomizada → labirinto **perfeito** (um único caminho entre dois pontos).
- **Aberturas** removem paredes internas ao acaso → surgem ciclos → passa a existir caminho mais curto e mais longo. É isso que torna o Dijkstra interessante.
- **Lama** torna o custo diferente do número de passos → mostra a diferença entre "menor caminho" e "menor custo".
- **Semente** controla todas as escolhas aleatórias (geradores separados por parâmetro, então mudar a lama não altera o desenho do labirinto).

## Algoritmos: o que cada um emite

| Evento | Dijkstra | Backtracking | Q-Learning (S3, previsto) |
|---|---|---|---|
| `frontier` | célula entrou na fila de prioridade (com distância) | — | — |
| `visit` | célula retirada da fila (expandida) | chamada recursiva (empilha) | agente se move |
| `backtrack` | — | retorno da recursão (desempilha) | — |
| `path` | caminho ótimo reconstruído | pilha final = caminho | política aprendida (gulosa) |
| `done`/`fail` | custo e passos | custo e passos | recompensa média, episódios |

## Desenho previsto do Q-Learning (Sprint 3)

- **Estado:** célula `(x, y)`. **Ações:** cima, direita, baixo, esquerda.
- **Recompensas (configuráveis):** objetivo +100; passo −1; lama −5; bater na parede −10 (fica no lugar).
- **Atualização:** `Q(s,a) ← Q(s,a) + α · [r + γ · maxₐ' Q(s',a') − Q(s,a)]`
- **Exploração:** ε-greedy com decaimento por episódio.
- **Parâmetros na interface:** α, γ, ε inicial, decaimento de ε, nº de episódios, máximo de passos por episódio.
- **Visualização:** cor de cada célula = `max Q` (mapa de calor), seta = melhor ação, gráfico de recompensa por episódio, botão "assistir agente".
- O treino também é um gerador: emite um evento por passo do agente ou por episódio (configurável), para manter a interface responsiva no navegador.

## Fluxo de build e publicação (a partir da S1)

```mermaid
flowchart LR
    A[Código no GitHub] --> B[pytest]
    B -- passou --> C["pygbag --build app"]
    C --> D[build/web: index.html + .apk]
    D --> E[GitHub Pages]
    E --> F([Link enviado aos stakeholders])
    B -- falhou --> G[Corrigir antes da Review]
```
