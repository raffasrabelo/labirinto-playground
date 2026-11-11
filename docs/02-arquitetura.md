# 02 · Arquitetura e Fluxos da Plataforma

## Tecnologias

| Camada | Tecnologia | Por quê |
|---|---|---|
| Lógica (algoritmos, labirinto, sessão) | Python 3.12+ | Definida no TCC; sintaxe próxima do pseudocódigo das disciplinas |
| Visualização do labirinto | **pygame-ce** (Community Edition do Pygame) | Desenho e edição da grade; é a versão usada pelo pygbag |
| Interface (controles, métricas, legenda) | **HTML + CSS + JavaScript** | Componentes nativos do navegador, tipografia nítida, layout responsivo e acessível |
| Execução no navegador | **pygbag** (Python/Pygame → WebAssembly) | Roda o Python no navegador, sem instalação |
| Testes | pytest | Valida a lógica sem abrir janela nem navegador |
| Publicação | GitHub Actions + GitHub Pages | Link público atualizado a cada push |

## Decisões de arquitetura (ADR)

### ADR-01 · Algoritmos como geradores de eventos (Sprint 0)
Cada algoritmo é uma função geradora que, a cada `yield`, devolve um `Event`
(`frontier`, `visit`, `backtrack`, `path`, `done`, `fail`). O algoritmo **não sabe desenhar**
e a interface **não sabe resolver labirintos**. Com isso:
1. **Passo a passo de graça:** pausar é parar de chamar `next()`.
2. **Velocidade ajustável:** a interface consome N eventos por segundo.
3. **Testabilidade:** os testes executam o gerador até o fim e conferem o resultado.
4. **Extensibilidade:** um algoritmo novo é só mais um gerador registrado em `algorithms/__init__.py`.

### ADR-02 · Interface híbrida: Pygame só no labirinto, HTML/CSS no restante (Sprint 0, 27/10)
**Contexto.** A v0.1 desenhava toda a interface em Pygame. Os algoritmos funcionavam, mas o
visual ficou fraco:
- o Pygame não tem componentes de interface;
- a única fonte disponível no navegador é a FreeSansBold, toda em negrito;
- o pygbag esticava uma imagem fixa de 1280×760, deixando o texto borrado.

**Decisão.** O Pygame desenha **apenas o labirinto** (grade, estados das células e edição com
o mouse). Parâmetros, botões, métricas, legenda e textos passam para HTML/CSS/JavaScript. As
duas partes conversam por uma ponte de mensagens JSON.

**Alternativas avaliadas.**
- (A) Polir a interface dentro do Pygame: o teto de qualidade era limitado.
- (C) Interface 100% web com Pyodide: o Pygame sairia do projeto, alterando os objetivos do TCC.

As posições abaixo são estimativas qualitativas da equipe, não medições. Os rótulos estão
sem acento porque este tipo de gráfico do Mermaid não aceita caracteres acentuados.

```mermaid
quadrantChart
    title Alternativas para a interface (ADR-02)
    x-axis Pouco impacto no TCC --> Muito impacto no TCC
    y-axis Qualidade visual baixa --> Qualidade visual alta
    quadrant-1 Muda o projeto
    quadrant-2 Melhor escolha
    quadrant-3 Resultado fraco
    quadrant-4 Evitar
    v0.1 tudo em Pygame: [0.2, 0.15]
    A polir no Pygame: [0.22, 0.4]
    B Pygame e HTML - escolhida: [0.3, 0.8]
    C web com Pyodide: [0.88, 0.9]
```

**Consequências.**
- ✅ Interface com qualidade de site moderno, responsiva e acessível.
- ✅ O canvas é desenhado na resolução física da tela, então o labirinto fica nítido.
- ✅ O Pygame continua sendo a tecnologia de visualização (objetivo específico 2 mantido).
- ⚠️ A versão desktop vira apenas ferramenta de desenvolvimento: só o labirinto e atalhos de teclado.
- ⚠️ Mais uma linguagem no projeto (JavaScript). Optou-se por JavaScript puro, sem TypeScript,
  porque o código da página é pequeno (~200 linhas) e assim não é preciso Node.js nem etapa de
  compilação. TypeScript pode ser adotado se a interface crescer.

## Visão em camadas

```mermaid
flowchart TB
    subgraph Pagina["Página web (web/src/)"]
        HTML["template.html<br/>estrutura"]
        CSS["style.css<br/>design"]
        JS["app.js<br/>eventos + renderização do estado"]
    end
    subgraph Python["Python no navegador (pygbag) - app/"]
        MAIN["main.py<br/>laço + ponte (WebBridge)"]
        subgraph CORE["core/ (Python puro)"]
            S["session.py<br/>comandos e retrato do estado"]
            G["grid.py / maze.py"]
            RS["run_state.py"]
        end
        subgraph ALG["algorithms/ (Python puro)"]
            D["dijkstra.py"]
            BT["backtracking.py"]
            Q["qlearning.py"]
        end
        BV["ui/board.py<br/>desenho do labirinto (Pygame)"]
    end
    JS -- "comandos JSON<br/>labirinto.pull()" --> MAIN
    MAIN -- "estado JSON<br/>labirinto.push()" --> JS
    MAIN --> S
    MAIN --> BV
    BV -- "mouse: editar células" --> S
    S --> G & RS
    S -- "next(gerador)" --> D & BT & Q
    BV -. "desenha no" .-> CANVAS[("canvas #canvas<br/>dentro da página")]
    TESTS["tests/ (pytest)"] -.-> CORE & ALG
```

## Estrutura de pastas

```
app/                       # tudo que é empacotado pelo pygbag
├── main.py                # laço assíncrono + ponte (web) ou teclado (desktop)
├── algorithms/            # geradores de eventos (Dijkstra, Backtracking...)
├── core/
│   ├── grid.py            # modelo do labirinto
│   ├── maze.py            # geração com semente
│   ├── run_state.py       # aplica eventos -> estado desenhável
│   └── session.py         # parâmetros, comandos, execução, retrato do estado
├── ui/
│   ├── board.py           # desenho do labirinto + edição com o mouse
│   └── theme.py           # cores do labirinto (espelham o CSS)
└── tests/                 # pytest: algoritmos e sessão
web/src/                   # interface da página
├── template.html          # estrutura + bloco exigido pelo pygbag
├── style.css              # design system (tokens de cor, tipografia, layout)
└── app.js                 # ponte JS + eventos dos controles
tools/build_web.py         # junta HTML+CSS+JS e chama o pygbag
```

## Modelo de classes (Python)

Os algoritmos são **funções geradoras**, não classes. Eles aparecem pelo registro
`AlgorithmInfo.run`. `generate_maze()` é uma função que devolve um `Grid` pronto.

```mermaid
classDiagram
    direction LR
    class Session {
        +dict params
        +Grid grid
        +RunState run
        +str mode
        +int maze_version
        +command(cmd)
        +set_param(name, value)
        +toggle_play()
        +step()
        +update(dt)
        +edit_begin(cell, erase)
        +edit_drag(cell)
        +edit_end()
        +snapshot() dict
    }
    class Grid {
        +int cols
        +int rows
        +tuple start
        +tuple goal
        +get(cell) int
        +set(cell, kind)
        +neighbors(cell) list
        +cost(cell) int
        +path_cost(path) int
        +move_endpoint(which, cell)
    }
    class RunState {
        +dict cells
        +dict dist
        +int steps
        +int visited
        +int depth
        +list path
        +bool found
        +apply(event)
    }
    class Event {
        <<dataclass>>
        +str kind
        +tuple cell
        +dict data
    }
    class AlgorithmInfo {
        <<dataclass>>
        +str name
        +function run
        +str description
        +bool available
    }
    class BoardView {
        +Session session
        +handle(ev)
        +draw(surface)
        +cell_at(pos) tuple
    }
    class WebBridge {
        +pull() list
        +push(snapshot)
    }
    class DesktopBridge {
        +key(ev)
        +pull() list
        +push(snapshot)
    }
    Session *-- Grid : contém
    Session *-- RunState : contém
    Session ..> AlgorithmInfo : consulta o registro
    AlgorithmInfo ..> Event : o gerador emite
    RunState ..> Event : aplica
    BoardView --> Session : desenha e edita
    WebBridge ..> Session : comandos e retrato
    DesktopBridge ..> Session : comandos e retrato
```

## Ponte JavaScript ↔ Python

O Python, a cada quadro (60 vezes por segundo):
1. chama `window.labirinto.pull()`, que devolve a fila de comandos da página em JSON (ou `""`);
2. aplica os comandos na `Session`;
3. desenha o labirinto;
4. chama `window.labirinto.push(estadoJSON)`, **apenas se o estado mudou**.

**Comandos (página → Python)**

| Comando | Exemplo |
|---|---|
| Alterar parâmetro | `{"type": "set", "name": "size", "value": 31}`. Nomes: `algorithm`, `size`, `openness`, `mud`, `seed`, `speed`, `brush`, `show_numbers` |
| Executar / pausar | `{"type": "play"}` |
| Um passo | `{"type": "step"}` |
| Reiniciar | `{"type": "reset"}` |
| Novo labirinto (semente aleatória) | `{"type": "new_maze"}` |
| Grade vazia | `{"type": "clear"}` |
| Tamanho do quadro | `{"type": "resize", "w": 1292, "h": 1292}` (pixels físicos = CSS × devicePixelRatio) |

Todos os valores são validados no Python (`Session.set_param`): limites, tamanho ímpar,
algoritmo disponível. A página nunca é a fonte da verdade.

**Estado (Python → página)**

```json
{
  "mode": "running",
  "status": "running",
  "params": {"algorithm": "dijkstra", "size": 21, "openness": 10, "mud": 15,
             "seed": 42, "speed": 20, "brush": "wall", "show_numbers": true},
  "description": "Expande sempre a célula de MENOR custo acumulado...",
  "metrics": {"steps": 80, "visited": 39, "frontier": 2, "depth": 0,
              "max_depth": 0, "moves": null, "cost": null}
}
```
`status` pode ser `idle`, `running`, `paused`, `found` ou `no_path`.

## Carregamento da página

A interface aparece logo; os controles só são ativados quando o Python envia o primeiro estado.

```mermaid
sequenceDiagram
    actor U as Aluno
    participant N as Navegador
    participant GP as GitHub Pages
    participant CDN as CDN do pygbag
    participant JS as app.js
    participant PY as Python (WebAssembly)
    U->>N: abre o link
    N->>GP: GET index.html (estrutura + CSS + JS)
    N->>JS: executa app.js
    JS->>JS: cria window.labirinto e mede o quadro
    Note over N,JS: interface visível, controles desativados,<br/>"Carregando o Python no navegador..."
    N->>CDN: runtime + CPython 3.12 em WebAssembly
    N->>GP: GET app.tar.gz (código do app)
    N->>CDN: pygame-ce para WebAssembly
    N->>PY: executa main.py
    PY->>JS: pull()
    JS-->>PY: [{"type": "resize", ...}]
    PY->>PY: cria o canvas no tamanho físico do quadro
    PY->>JS: push(estado inicial)
    JS->>N: esconde o carregador e ativa os controles
    U->>N: interage
```

## Fluxo de uso (jornada do aluno)

```mermaid
flowchart LR
    A([Abre o link]) --> B[Escolhe o algoritmo]
    B --> C[Ajusta parâmetros<br/>tamanho, aberturas, lama, semente]
    C --> D[Desenha no labirinto<br/>paredes, lama, início/objetivo]
    D --> E[Executa ou avança passo a passo]
    E --> F[Observa cores, números,<br/>métricas e explicação]
    F --> G{Entendeu?}
    G -- "não" --> H[Reduz a velocidade<br/>ou usa Passo]
    H --> E
    G -- "quer comparar" --> I[Troca o algoritmo<br/>mantendo a semente]
    I --> E
    G -- "quer testar hipótese" --> C
```

## Ciclo de execução

```mermaid
sequenceDiagram
    actor U as Aluno
    participant H as Página (app.js)
    participant M as main.py
    participant S as Session
    participant A as Algoritmo (gerador)
    participant B as BoardView (Pygame)
    U->>H: clica "Executar"
    H->>H: fila += {"type":"play"}
    loop a cada quadro (60x/s)
        M->>H: pull()
        H-->>M: [{"type":"play"}]
        M->>S: command(play)
        Note over S: n = velocidade × Δt
        loop n vezes
            S->>A: next()
            A-->>S: Event
        end
        M->>B: draw(canvas)
        M->>H: push(estado) se mudou
        H->>U: métricas, status, botões
    end
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

| Evento | Dijkstra | Backtracking | Q-Learning |
|---|---|---|---|
| `frontier` | célula entrou na fila de prioridade (com distância) | — | — |
| `visit` | célula retirada da fila (expandida) | chamada recursiva (empilha) | — |
| `backtrack` | — | retorno da recursão (desempilha) | — |
| `agent` | — | — | o agente deu um passo (o 1º de cada episódio leva a tabela Q, o nº do episódio e o ε) |
| `episode` | — | — | fim de um episódio: recompensa total, passos, se chegou ao objetivo, ε |
| `path` | caminho ótimo reconstruído | pilha final = caminho | percurso seguindo a política aprendida (sempre a ação de maior Q) |
| `done`/`fail` | custo e passos | custo e passos | custo e passos da política; `fail` se ela não chega ao objetivo |

## Q-Learning (implementado na v0.3, 11/11)

- **Estado:** célula `(x, y)`. **Ações:** cima, direita, baixo, esquerda.
- **Recompensas:** entrar numa célula custa o mesmo que nos outros algoritmos (livre −1,
  lama −5); bater na parede vale −penalidade (padrão 10) e o agente fica no lugar; chegar ao
  objetivo vale +recompensa (padrão 100) e encerra o episódio.
- **Atualização:** `Q(s,a) ← Q(s,a) + α · [r + γ · maxₐ' Q(s',a') − Q(s,a)]`; no objetivo, o alvo é só `r`.
- **Exploração:** ε-greedy; ε é multiplicado pelo decaimento a cada episódio (mínimo 0,01).
- **Limite de passos por episódio:** `max(200, 4 × células livres)`.
- **Valores padrão** (α 0,5; γ 0,995; ε 0,3; decaimento 0,99; 200 episódios): escolhidos por
  experimento, ver [06-algoritmos.md](06-algoritmos.md#q-learning-escolha-dos-valores-padrão).
- **Reprodutível:** o gerador aleatório do agente usa a semente do labirinto.
- **Visualização no Pygame:** mapa de calor violeta com o valor `max Q` de cada célula
  (normalizado entre o menor e o maior valor), seta com a melhor ação e o agente como um
  círculo laranja. **Na página:** parâmetros, métricas do treino e gráfico SVG da recompensa
  por episódio (série reduzida a no máximo 200 pontos, com média móvel).
- **Desempenho:** a sessão processa eventos até ~12 ms por quadro e descarta o atraso
  acumulado, então a página continua fluida a 100.000 passos/s. Medido no navegador: o treino
  completo do labirinto 21 × 21 da demo (48.761 eventos) termina em menos de 1 segundo na
  velocidade máxima.

Novos parâmetros aceitos por `{"type": "set"}`: `alpha`, `gamma`, `epsilon`, `decay`,
`episodes`, `goal_reward`, `wall_penalty`, `show_policy`. Novos campos do estado:
`metrics.episode`, `metrics.episodes`, `metrics.epsilon`, `metrics.episode_steps`,
`metrics.last_reward`, `metrics.reached` e a lista `rewards`.

## Implantação: onde cada parte roda

```mermaid
flowchart LR
    subgraph DEV["Computador da equipe"]
        CODE["código + docs"]
        LOCAL["tools/build_web.py --serve<br/>localhost:8000"]
    end
    subgraph GH["GitHub"]
        REPO[("repositório<br/>raffasrabelo/labirinto-playground")]
        ACT["Actions<br/>test → build → deploy"]
        PAGES["Pages<br/>index.html + app.tar.gz"]
    end
    CDN["CDN pygame-web.github.io<br/>CPython + pygame-ce (WASM)"]
    FONTS["Google Fonts<br/>fonte Inter"]
    subgraph USER["Navegador do aluno"]
        PAGE["Página<br/>HTML + CSS + JS"]
        WASM["Python + Pygame<br/>em WebAssembly"]
    end
    CODE -- "git push" --> REPO --> ACT --> PAGES
    CODE --> LOCAL
    PAGES -- "HTTPS" --> PAGE
    CDN -- "runtime" --> WASM
    FONTS --> PAGE
    PAGE <-->|ponte JSON| WASM
```

Tudo roda no navegador do aluno: não há servidor de aplicação nem banco de dados. O GitHub
Pages só entrega arquivos estáticos.

## Fluxo de build e publicação

```mermaid
flowchart LR
    A[push na main] --> B[pytest]
    B -- passou --> C["tools/build_web.py<br/>HTML+CSS+JS → template<br/>pygbag --build"]
    C --> D[app/build/web]
    D --> E[GitHub Pages]
    E --> F([Link enviado aos stakeholders])
    B -- falhou --> G[nada é publicado]
```
