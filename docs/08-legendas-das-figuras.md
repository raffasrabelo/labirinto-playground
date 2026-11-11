# 08 · Legendas das Figuras (padrão ABNT)

Legendas prontas para todas as imagens e diagramas do projeto. Para cada figura há:
- **Legenda:** o título, que vai **acima** da figura, depois de "Figura N –";
- **Fonte:** vai **abaixo** da figura;
- **Chamada:** uma sugestão de frase para citar a figura no texto. Pela ABNT, toda figura
  deve ser citada no texto antes de aparecer.

**No Word:** clique na imagem → *Referências → Inserir Legenda* → rótulo "Figura", posição
"Acima do item selecionado". O número é automático; cole só o título depois do travessão.
Para a fonte, use um parágrafo logo abaixo da imagem, em fonte menor (10 pt).

> As figuras estão em ordem temática, não na ordem em que vão aparecer no TCC. A coluna
> "Seção sugerida" do [índice de diagramas](07-diagramas.md) ajuda a posicioná-las.

---

## A. Capturas de tela da plataforma

As capturas da v0.1 e da v0.2 usam **exatamente os mesmos parâmetros** (grade 21×21,
aberturas 10%, lama 15%, semente 42) e mostram os mesmos resultados, para que a comparação
evidencie só a mudança de interface.

### A1 · v0.1: Dijkstra em execução
- **Arquivo:** `docs/img/v0.1-dijkstra-execucao.png`
- **Legenda:** Protótipo v0.1: algoritmo de Dijkstra em execução, com a interface inteiramente desenhada em Pygame
- **Fonte:** Elaborado pelos autores (2026).
- **Chamada:** "A Figura N apresenta o primeiro protótipo (v0.1) durante a execução do
  algoritmo de Dijkstra. Nessa versão, painéis, botões e textos eram desenhados com a
  biblioteca Pygame."

### A2 · v0.1: Dijkstra concluído
- **Arquivo:** `docs/img/v0.1-dijkstra-concluido.png`
- **Legenda:** Protótipo v0.1: caminho de menor custo encontrado pelo algoritmo de Dijkstra (grade 21 × 21, semente 42)
- **Fonte:** Elaborado pelos autores (2026).
- **Chamada:** "Ao final da execução (Figura N), o algoritmo expandiu 232 células e
  encontrou um caminho de 56 passos com custo 120."

### A3 · v0.1: Backtracking em grade 41 × 41
- **Arquivo:** `docs/img/v0.1-backtracking-41x41.png`
- **Legenda:** Protótipo v0.1: caminho encontrado pelo Backtracking em grade 41 × 41, com os retrocessos destacados em vermelho
- **Fonte:** Elaborado pelos autores (2026).
- **Chamada:** "Na Figura N, as células em vermelho indicam os retrocessos do Backtracking
  ao encontrar becos sem saída."

### A4 · v0.2: Dijkstra em execução
- **Arquivo:** `docs/img/v0.2-dijkstra-execucao.png`
- **Legenda:** Versão 0.2: algoritmo de Dijkstra em execução após 120 eventos, com interface em HTML/CSS e labirinto desenhado em Pygame
- **Fonte:** Elaborado pelos autores (2026).
- **Chamada:** "A Figura N mostra a mesma situação da Figura N (v0.1) na versão 0.2. Os
  controles de execução passaram para o topo, os parâmetros ficaram à esquerda e as métricas
  foram reorganizadas em cartões à direita. A célula atual aparece destacada em laranja e os
  números indicam a distância acumulada desde o início."

### A5 · v0.2: Dijkstra concluído
- **Arquivo:** `docs/img/v0.2-dijkstra-concluido.png`
- **Legenda:** Versão 0.2: caminho de menor custo encontrado pelo algoritmo de Dijkstra (grade 21 × 21, semente 42)
- **Fonte:** Elaborado pelos autores (2026).
- **Chamada:** "Os resultados da versão 0.2 (Figura N) são idênticos aos da v0.1: 232
  células expandidas, 56 passos e custo 120. Isso confirma que a reformulação da interface
  não alterou a lógica dos algoritmos."

### A6 · v0.2: Backtracking em grade 41 × 41
- **Arquivo:** `docs/img/v0.2-backtracking-41x41.png`
- **Legenda:** Versão 0.2: caminho encontrado pelo Backtracking em grade 41 × 41, com a profundidade da pilha de recursão exibida nas métricas
- **Fonte:** Elaborado pelos autores (2026).
- **Chamada:** "Na versão 0.2 (Figura N), a legenda passa a exibir apenas os estados do
  algoritmo selecionado (como *Retrocesso*), e o painel de resultados mostra o tamanho atual
  e o máximo da pilha de recursão (169)."

### A7 · v0.2: versão para celular
- **Arquivo:** `docs/img/v0.2-celular.png`
- **Legenda:** Versão 0.2 exibida em tela de celular (390 pixels de largura)
- **Fonte:** Elaborado pelos autores (2026).
- **Chamada:** "Por ser construída com HTML e CSS responsivos, a interface se reorganiza em
  uma coluna em telas pequenas, mantendo o labirinto legível (Figura N)."
- **Dica:** insira com cerca de 6 cm de largura.

### A8 · Comparação v0.1 × v0.2
- **Arquivo:** `docs/img/comparacao-v0.1-v0.2.png`
- **Legenda:** Comparação entre as interfaces das versões 0.1 e 0.2 em uma mesma execução do algoritmo de Dijkstra
- **Fonte:** Elaborado pelos autores (2026).
- **Chamada:** "A Figura N compara as duas versões em uma mesma execução. Os resultados
  coincidem, mas a versão 0.2, cuja interface foi refeita em HTML/CSS após a avaliação do
  protótipo, apresenta tipografia nítida, hierarquia visual entre controles, parâmetros e
  resultados, e legenda adaptada ao algoritmo."

### A9 · v0.3: Q-Learning em treinamento
- **Arquivo:** `docs/img/v0.3-qlearning-treinando.png`
- **Legenda:** Versão 0.3: agente de Q-Learning em treinamento, com o valor aprendido em cada célula e a melhor ação indicada por setas
- **Fonte:** Elaborado pelos autores (2026).
- **Chamada:** "Durante o treinamento (Figura N), o valor aprendido se espalha a partir do
  objetivo: as células mais escuras ficam próximas à saída. O gráfico de recompensa por
  episódio mostra o agente melhorando à medida que a exploração diminui."

### A10 · v0.3: Q-Learning concluído
- **Arquivo:** `docs/img/v0.3-qlearning-concluido.png`
- **Legenda:** Versão 0.3: caminho percorrido pelo agente de Q-Learning seguindo a política aprendida (grade 21 × 21, semente 42)
- **Fonte:** Elaborado pelos autores (2026).
- **Chamada:** "Ao final de 200 episódios (Figura N), o agente percorre o labirinto seguindo
  a política aprendida e obtém custo 120, o mesmo do Dijkstra, sem conhecer o mapa
  previamente."

### A11 · v0.3: efeito do fator de desconto
- **Arquivo:** `docs/img/v0.3-qlearning-gama-095.png`
- **Legenda:** Versão 0.3: com fator de desconto γ = 0,95, o agente não aprende o caminho na grade 21 × 21
- **Fonte:** Elaborado pelos autores (2026).
- **Chamada:** "Reduzir o fator de desconto para 0,95 (Figura N) torna o agente 'míope': a
  recompensa do objetivo, descontada ao longo de dezenas de passos, deixa de compensar o
  custo do caminho, e a política aprendida não chega à saída."

---

## B. Metodologia e processo (Scrum)

### B1 · Visão geral do Scrum no projeto
- **Onde está:** [03 · Visão geral](03-processo-de-trabalho.md#visão-geral-do-scrum-no-projeto)
- **Legenda:** Papéis, eventos e artefatos do Scrum adaptado ao projeto
- **Fonte:** Elaborado pelos autores (2026).
- **Chamada:** "A Figura N resume a adaptação do Scrum a uma equipe de dois integrantes,
  relacionando papéis, eventos e artefatos."

### B2 · Ciclo da sprint
- **Arquivo:** `docs/img/scrum-ciclo-da-sprint.png` (ou `.svg`)
- **Legenda:** Ciclo de uma sprint de uma semana adotado no projeto
- **Fonte:** Elaborado pelos autores (2026).
- **Chamada:** "Cada sprint dura uma semana, de quinta a quarta-feira, e segue o ciclo da
  Figura N. O trabalho só é apresentado na Sprint Review depois de atender à *Definition of
  Done*, e o feedback recebido realimenta o Product Backlog."

### B3 · Quem faz o quê
- **Onde está:** [03 · Quem faz o quê](03-processo-de-trabalho.md#quem-faz-o-quê)
- **Legenda:** Responsabilidades de cada participante ao longo de uma sprint
- **Fonte:** Elaborado pelos autores (2026).
- **Chamada:** "A Figura N detalha a participação de stakeholders, Product Owner, equipe,
  assistente de IA e GitHub em cada etapa da sprint."

### B4 · Semana típica de sprint
- **Onde está:** [03 · Semana típica](03-processo-de-trabalho.md#semana-típica-de-sprint)
- **Legenda:** Distribuição das atividades em uma semana típica de sprint (exemplo: Sprint 1)
- **Fonte:** Elaborado pelos autores (2026).
- **Chamada:** "A Figura N mostra como as atividades se distribuem nos dias úteis de uma
  sprint, com desenvolvimento e escrita do TCC em paralelo."

### B5 · Ciclo de vida de um item do backlog
- **Onde está:** [03 · Ciclo de vida](03-processo-de-trabalho.md#ciclo-de-vida-de-um-item-do-backlog)
- **Legenda:** Estados de um item do Product Backlog, da ideia à demonstração
- **Fonte:** Elaborado pelos autores (2026).
- **Chamada:** "Cada item do backlog percorre os estados da Figura N e só é considerado
  pronto quando atende a todos os critérios da *Definition of Done*."

### B6 · Fluxo do feedback
- **Onde está:** [03 · Fluxo do feedback](03-processo-de-trabalho.md#fluxo-do-feedback)
- **Legenda:** Tratamento do feedback recebido dos stakeholders
- **Fonte:** Elaborado pelos autores (2026).
- **Chamada:** "O feedback dos stakeholders é classificado e encaminhado conforme a
  Figura N."

### B7 · Fluxo de versionamento
- **Onde está:** [03 · Fluxo de código](03-processo-de-trabalho.md#fluxo-de-código-git)
- **Legenda:** Fluxo de versionamento previsto, com branches por item e tags por sprint
- **Fonte:** Elaborado pelos autores (2026).
- **Chamada:** "O código é versionado com Git seguindo o fluxo da Figura N; cada sprint
  encerrada recebe uma tag, o que permite recuperar qualquer incremento."

### B8 · Uso de IA e registro de prompts
- **Onde está:** [03 · Uso de IA](03-processo-de-trabalho.md#uso-de-ia-generativa-no-projeto)
- **Legenda:** Fluxo de uso do assistente de inteligência artificial e de registro dos prompts
- **Fonte:** Elaborado pelos autores (2026).
- **Chamada:** "O uso do assistente de IA seguiu o fluxo da Figura N: todo resultado foi
  revisado e testado pelos autores e registrado no Apêndice X."

### B9 · Cronograma
- **Onde está:** [04 · Visão geral](04-cronograma.md#visão-geral)
- **Legenda:** Cronograma das sprints e da escrita do TCC (outubro e novembro de 2026)
- **Fonte:** Elaborado pelos autores (2026).
- **Chamada:** "O desenvolvimento foi organizado em seis sprints semanais, conforme o
  cronograma da Figura N."

### B10 · Marcos e decisões
- **Onde está:** [04 · Linha do tempo](04-cronograma.md#linha-do-tempo-de-marcos-e-decisões)
- **Legenda:** Marcos e decisões ao longo do desenvolvimento da plataforma
- **Fonte:** Elaborado pelos autores (2026).
- **Chamada:** "A Figura N registra os principais marcos do desenvolvimento, entre eles a
  decisão de reformular a interface ainda na Sprint 0."

---

## C. Requisitos

### C1 · Casos de uso
- **Arquivo:** `docs/img/casos-de-uso.svg`
- **Legenda:** Diagrama de casos de uso da plataforma
- **Fonte:** Elaborado pelos autores (2026).
- **Chamada:** "A Figura N apresenta os casos de uso da plataforma. O professor herda as
  funcionalidades do estudante e pode usá-las para demonstrações em aula."

### C2 · Rastreabilidade
- **Onde está:** [01 · Rastreabilidade](01-visao-e-requisitos.md#rastreabilidade-objetivos-do-tcc--requisitos--entregas)
- **Legenda:** Rastreabilidade entre os objetivos específicos, os requisitos e as entregas do projeto
- **Fonte:** Elaborado pelos autores (2026).
- **Chamada:** "A Figura N relaciona cada objetivo específico aos requisitos e às entregas
  que o comprovam."

---

## D. Arquitetura

### D1 · Alternativas de interface (ADR-02)
- **Onde está:** [02 · ADR-02](02-arquitetura.md#adr-02--interface-híbrida-pygame-só-no-labirinto-htmlcss-no-restante-sprint-0-2710)
- **Legenda:** Comparação das alternativas de interface consideradas, segundo impacto no projeto e qualidade visual
- **Fonte:** Elaborado pelos autores (2026).
- **Nota (abaixo da fonte):** Posições estimadas qualitativamente pelos autores.
- **Chamada:** "Entre as alternativas da Figura N, optou-se pela interface híbrida, que
  oferece alta qualidade visual sem alterar as tecnologias previstas nos objetivos."

### D2 · Visão em camadas
- **Onde está:** [02 · Visão em camadas](02-arquitetura.md#visão-em-camadas)
- **Legenda:** Arquitetura em camadas da plataforma
- **Fonte:** Elaborado pelos autores (2026).
- **Chamada:** "Conforme a Figura N, a página em HTML/CSS/JavaScript comunica-se com o núcleo
  em Python por mensagens JSON; o Pygame é responsável apenas pelo desenho do labirinto."

### D3 · Modelo de classes
- **Onde está:** [02 · Modelo de classes](02-arquitetura.md#modelo-de-classes-python)
- **Legenda:** Diagrama de classes do núcleo da plataforma em Python
- **Fonte:** Elaborado pelos autores (2026).
- **Chamada:** "A Figura N apresenta as principais classes do núcleo. Os algoritmos são
  implementados como funções geradoras que emitem eventos."

### D4 · Carregamento da página
- **Onde está:** [02 · Carregamento](02-arquitetura.md#carregamento-da-página)
- **Legenda:** Sequência de carregamento da plataforma no navegador
- **Fonte:** Elaborado pelos autores (2026).
- **Chamada:** "Ao abrir a plataforma, o navegador obtém o interpretador Python compilado em
  WebAssembly e só então ativa os controles, conforme a Figura N."

### D5 · Jornada do estudante
- **Onde está:** [02 · Fluxo de uso](02-arquitetura.md#fluxo-de-uso-jornada-do-aluno)
- **Legenda:** Fluxo de uso da plataforma pelo estudante
- **Fonte:** Elaborado pelos autores (2026).
- **Chamada:** "O uso previsto da plataforma segue o ciclo exploratório da Figura N: ajustar
  parâmetros, executar, observar e comparar."

### D6 · Ciclo de execução
- **Onde está:** [02 · Ciclo de execução](02-arquitetura.md#ciclo-de-execução)
- **Legenda:** Troca de mensagens entre a página e o Python a cada quadro de execução
- **Fonte:** Elaborado pelos autores (2026).
- **Chamada:** "A cada quadro, a página e o Python trocam mensagens como mostra a Figura N."

### D7 · Estados da execução
- **Onde está:** [02 · Estados da execução](02-arquitetura.md#estados-da-execução)
- **Legenda:** Estados de execução de um algoritmo na plataforma
- **Fonte:** Elaborado pelos autores (2026).
- **Chamada:** "A execução de um algoritmo pode ser pausada, avançada passo a passo ou
  reiniciada, conforme os estados da Figura N."

### D8 · Implantação
- **Onde está:** [02 · Implantação](02-arquitetura.md#implantação-onde-cada-parte-roda)
- **Legenda:** Diagrama de implantação da plataforma
- **Fonte:** Elaborado pelos autores (2026).
- **Chamada:** "Toda a execução ocorre no navegador do estudante; o GitHub Pages apenas
  disponibiliza os arquivos estáticos (Figura N)."

### D9 · Build e publicação
- **Onde está:** [02 · Build e publicação](02-arquitetura.md#fluxo-de-build-e-publicação)
- **Legenda:** Fluxo de integração contínua e publicação da plataforma
- **Fonte:** Elaborado pelos autores (2026).
- **Chamada:** "Cada alteração enviada ao repositório passa pelos testes automatizados antes
  de ser publicada (Figura N)."

### D10 · Pipeline do GitHub Actions
- **Onde está:** [P02](prompts/P02-github-pages.md)
- **Legenda:** Etapas do pipeline de testes e publicação no GitHub Actions
- **Fonte:** Elaborado pelos autores (2026).
- **Chamada:** "O pipeline da Figura N impede a publicação de versões com testes falhando."

---

## E. Algoritmos

### E1 · Mapa conceitual
- **Onde está:** [06 · Mapa conceitual](06-algoritmos.md#mapa-conceitual)
- **Legenda:** Mapa conceitual dos algoritmos abordados na plataforma
- **Fonte:** Elaborado pelos autores (2026).
- **Chamada:** "A Figura N relaciona cada algoritmo ao seu paradigma, à estrutura de dados
  utilizada e à garantia que oferece."

### E2 · Geração do labirinto
- **Onde está:** [06 · Geração do labirinto](06-algoritmos.md#geração-do-labirinto-busca-em-profundidade-randomizada)
- **Legenda:** Fluxograma da geração de labirintos por busca em profundidade randomizada
- **Fonte:** Elaborado pelos autores (2026).
- **Chamada:** "Os labirintos são gerados pelo procedimento da Figura N, que é, ele próprio,
  uma forma de backtracking."

### E3 · Backtracking
- **Onde está:** [06 · Backtracking](06-algoritmos.md#backtracking)
- **Legenda:** Fluxograma do algoritmo de Backtracking em sua forma recursiva
- **Fonte:** Elaborado pelos autores (2026).
- **Chamada:** "A Figura N descreve o Backtracking: o algoritmo avança enquanto há vizinhos
  livres e retrocede ao encontrar um beco sem saída."

### E4 · Dijkstra
- **Onde está:** [06 · Dijkstra](06-algoritmos.md#dijkstra)
- **Legenda:** Fluxograma do algoritmo de Dijkstra
- **Fonte:** Elaborado pelos autores (2026). Adaptado de Dijkstra (1959). *(ver observação ao final)*
- **Chamada:** "O algoritmo de Dijkstra (Figura N) expande sempre a célula de menor custo
  acumulado, retirada de uma fila de prioridade."

### E5 · Q-Learning
- **Onde está:** [06 · Q-Learning](06-algoritmos.md#q-learning)
- **Legenda:** Fluxograma do treinamento do agente de Q-Learning
- **Fonte:** Elaborado pelos autores (2026). Adaptado de Watkins e Dayan (1992). *(ver observação ao final)*
- **Chamada:** "O treinamento do agente segue o laço da Figura N, que atualiza a tabela Q
  a cada passo com base na recompensa recebida."

### E6 · Custo do caminho por semente
- **Onde está:** [06 · Comparação](06-algoritmos.md#comparação-com-dados-reais-dijkstra--backtracking)
- **Legenda:** Custo do caminho encontrado pelos algoritmos de Dijkstra e Backtracking em dez labirintos
- **Fonte:** Dados da pesquisa (2026).
- **Nota (abaixo da fonte):** Barras: Dijkstra; linha: Backtracking. Grade 21 × 21, aberturas 10%, lama 15%, sementes 1 a 10.
- **Chamada:** "Como mostra a Figura N, o Dijkstra encontrou o caminho de menor custo em
  todos os casos, enquanto o Backtracking chegou a um custo até 2,7 vezes maior."

### E7 · Células expandidas por semente
- **Onde está:** [06 · Comparação](06-algoritmos.md#comparação-com-dados-reais-dijkstra--backtracking)
- **Legenda:** Células expandidas pelos algoritmos de Dijkstra e Backtracking em dez labirintos
- **Fonte:** Dados da pesquisa (2026).
- **Nota (abaixo da fonte):** Barras: Dijkstra; linha: Backtracking. Grade 21 × 21, aberturas 10%, lama 15%, sementes 1 a 10.
- **Chamada:** "Em média, o Backtracking expandiu menos células (Figura N), mas não em todos
  os casos: nas sementes 2 e 10, explorou mais que o Dijkstra e ainda encontrou caminhos
  mais caros."

---

## Observações

- **Referências dos algoritmos (E4 e E5):** as legendas sugerem "Adaptado de" os trabalhos
  originais: DIJKSTRA, E. W. *A note on two problems in connexion with graphs*. Numerische
  Mathematik, v. 1, p. 269–271, 1959; e WATKINS, C. J. C. H.; DAYAN, P. *Q-learning*. Machine
  Learning, v. 8, p. 279–292, 1992. **Confira essas referências antes de usar** e inclua-as na
  lista de Referências. Se preferir, use apenas "Elaborado pelos autores (2026)".
- **Fonte dos gráficos com dados:** "Dados da pesquisa" indica que os números foram gerados
  pelos próprios autores; o experimento é reproduzível com a plataforma.
- **Legenda dos gráficos E6 e E7:** o Mermaid não desenha legenda nesse tipo de gráfico, por
  isso ela entra como *Nota* abaixo da figura.
- **Exportar diagramas:** os diagramas da seção B a E (exceto C1 e B2, que já têm arquivo) estão
  em Mermaid. Exporte pelo <https://mermaid.live> ou peça a exportação em PNG/SVG, como foi
  feito com o ciclo da sprint.
