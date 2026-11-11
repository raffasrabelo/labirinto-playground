# 07 · Índice de Diagramas

Todos os diagramas do projeto, com o tipo escolhido e uma **sugestão de uso no TCC**. Serve de
ponto de partida para a lista de figuras. As legendas no padrão ABNT de todos eles (e das
capturas de tela) estão em [08 · Legendas das figuras](08-legendas-das-figuras.md).

## Por que estes tipos

| Tipo | Usado quando | Exemplo no projeto |
|---|---|---|
| Fluxograma (`flowchart`) | há passos e decisões | algoritmos, ciclo da sprint, feedback |
| Sequência (`sequenceDiagram`) | importa a **ordem das mensagens** entre participantes | ponte JS↔Python, carregamento, uso de IA |
| Sequência como raias | importa **quem** executa cada passo. O Mermaid não tem raias de verdade e o fluxograma com subgrafos ficou ilegível, então cada coluna faz o papel de uma raia | quem faz o quê na sprint |
| Estados (`stateDiagram`) | algo muda de situação ao longo do tempo | execução do algoritmo, item do backlog |
| Classes (`classDiagram`) | estrutura estática do código | modelo de classes Python |
| Gantt (`gantt`) | planejamento no calendário | cronograma, semana típica |
| Linha do tempo (`timeline`) | o que *aconteceu* em ordem | marcos e decisões |
| gitGraph | ramificações e versões do código | fluxo de branches e tags |
| Mapa mental (`mindmap`) | conceitos e suas relações | mapa conceitual dos algoritmos |
| Quadrantes (`quadrantChart`) | comparar alternativas em dois critérios | justificativa da ADR-02 |
| Gráfico (`xychart-beta`) | dados numéricos | Dijkstra × Backtracking |
| **UML de casos de uso (SVG)** | atores e funcionalidades. O Mermaid não tem esse tipo, por isso foi desenhado à mão em SVG | casos de uso |

## Catálogo

| # | Diagrama | Tipo | Onde está | Sugestão no TCC |
|---:|---|---|---|---|
| 1 | Visão geral do Scrum no projeto | fluxograma em blocos | [03](03-processo-de-trabalho.md#visão-geral-do-scrum-no-projeto) | 3.1 Metodologia |
| 2 | Ciclo da sprint (retrato, cabe em uma página) | fluxograma | [03](03-processo-de-trabalho.md#ciclo-da-sprint-1-semana-quinta--quarta) | 3.1 Metodologia (figura principal do Scrum) |
| 3 | Quem faz o quê | sequência (colunas = raias) | [03](03-processo-de-trabalho.md#quem-faz-o-quê) | 3.1 Metodologia |
| 4 | Semana típica de sprint | Gantt | [03](03-processo-de-trabalho.md#semana-típica-de-sprint) | Apêndice |
| 5 | Ciclo de vida de um item do backlog | estados | [03](03-processo-de-trabalho.md#ciclo-de-vida-de-um-item-do-backlog) | Apêndice |
| 6 | Fluxo do feedback | fluxograma de decisão | [03](03-processo-de-trabalho.md#fluxo-do-feedback) | 3.1 Metodologia |
| 7 | Fluxo de código (branches e tags) | gitGraph | [03](03-processo-de-trabalho.md#fluxo-de-código-git) | Apêndice |
| 8 | Uso de IA e registro de prompts | sequência | [03](03-processo-de-trabalho.md#uso-de-ia-generativa-no-projeto) | 3.1 Metodologia (declaração de uso de IA) |
| 9 | Cronograma das sprints | Gantt | [04](04-cronograma.md#visão-geral) | 3.1 Metodologia / Cronograma |
| 10 | Marcos e decisões | linha do tempo | [04](04-cronograma.md#linha-do-tempo-de-marcos-e-decisões) | 4 Resultados (narrativa do desenvolvimento) |
| 11 | Casos de uso | UML (SVG) | [01](01-visao-e-requisitos.md#casos-de-uso) · [arquivo](img/casos-de-uso.svg) | 3.x Requisitos |
| 12 | Rastreabilidade: objetivos → requisitos → entregas | fluxograma | [01](01-visao-e-requisitos.md#rastreabilidade-objetivos-do-tcc--requisitos--entregas) | 3.x Requisitos ou 5 Conclusão |
| 13 | Alternativas de interface (ADR-02) | quadrantes | [02](02-arquitetura.md#adr-02--interface-híbrida-pygame-só-no-labirinto-htmlcss-no-restante-sprint-0-2710) | 4 Resultados (decisão de projeto) |
| 14 | Visão em camadas | fluxograma | [02](02-arquitetura.md#visão-em-camadas) | 3.x Arquitetura |
| 15 | Modelo de classes | classes | [02](02-arquitetura.md#modelo-de-classes-python) | 3.x Arquitetura |
| 16 | Carregamento da página | sequência | [02](02-arquitetura.md#carregamento-da-página) | 3.x Arquitetura (WebAssembly) |
| 17 | Jornada do aluno | fluxograma | [02](02-arquitetura.md#fluxo-de-uso-jornada-do-aluno) | 3.x Requisitos ou 4 Resultados |
| 18 | Ciclo de execução (ponte JS↔Python) | sequência | [02](02-arquitetura.md#ciclo-de-execução) | 3.x Arquitetura |
| 19 | Estados da execução | estados | [02](02-arquitetura.md#estados-da-execução) | 3.x Arquitetura |
| 20 | Implantação | fluxograma | [02](02-arquitetura.md#implantação-onde-cada-parte-roda) | 3.x Arquitetura |
| 21 | Build e publicação | fluxograma | [02](02-arquitetura.md#fluxo-de-build-e-publicação) | Apêndice |
| 22 | Mapa conceitual dos algoritmos | mapa mental | [06](06-algoritmos.md#mapa-conceitual) | 3.1 (escolha dos algoritmos) |
| 23 | Geração do labirinto | fluxograma | [06](06-algoritmos.md#geração-do-labirinto-busca-em-profundidade-randomizada) | 3.x Desenvolvimento |
| 24 | Backtracking | fluxograma | [06](06-algoritmos.md#backtracking) | 2 Referencial ou 3.x Desenvolvimento |
| 25 | Dijkstra | fluxograma | [06](06-algoritmos.md#dijkstra) | 2 Referencial ou 3.x Desenvolvimento |
| 26 | Q-Learning (treino) | fluxograma | [06](06-algoritmos.md#q-learning) | 2 Referencial ou 3.x Desenvolvimento |
| 27 | Custo do caminho por semente | gráfico | [06](06-algoritmos.md#comparação-com-dados-reais-dijkstra--backtracking) | 4 Resultados |
| 28 | Células expandidas por semente | gráfico | [06](06-algoritmos.md#comparação-com-dados-reais-dijkstra--backtracking) | 4 Resultados |
| 29 | Pipeline do GitHub Actions | fluxograma | [P02](prompts/P02-github-pages.md) | Apêndice |

## Como levar um diagrama para o Word

1. **Mermaid:** copie o bloco de código (sem as crases) para <https://mermaid.live>, ajuste se
   quiser e use *Actions → SVG* (melhor qualidade) ou *PNG*. O Word aceita SVG desde a versão 2016.
2. **SVG (casos de uso):** insira `docs/img/casos-de-uso.svg` direto no Word (*Inserir → Imagens*).
3. Pela ABNT, a legenda fica **acima** da figura ("Figura N – Título") e a fonte **abaixo**
   ("Fonte: Elaborado pelos autores (2026)").
4. Ao alterar um diagrama aqui, exporte de novo. O arquivo `.md` é a fonte da verdade.

## Validação

Todos os diagramas Mermaid deste repositório foram renderizados sem erros com o Mermaid 10.9
(versão conservadora, compatível com o GitHub) em 28/10/2026.
