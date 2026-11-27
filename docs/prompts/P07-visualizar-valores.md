# P07 · Seletor "Visualizar no labirinto" (v0.4) e discussão do TCC

| Campo | Valor |
|---|---|
| Data | 27/11/2026 |
| Sprint | S4 |
| Item(ns) do backlog | US-29 (seletor), T-07 (discussão do TCC) |
| Autor do prompt | Rafael |
| Origem | **Sugestões do orientador** |
| Ferramenta / modelo | Claude Code (Claude Opus 5.5) |

## Prompt enviado

```text
Nosso orientador sugeriu que colocássemos um input para alterar o estado e mostrar o estado
de todas as células. A ideia é ter um select que altere o labirinto para os valores calculados.

E nos resultados do TCC, colocar pelo menos dois parágrafos de discussão para comparar o
sistema e resultados com outros trabalhos (buscar alguma coisa na literatura sobre a
importância de objetos de aprendizagem para algoritmos específicos para fazer essa
comparação/discussão)
```

## Parte 1 · Seletor "Visualizar no labirinto"

**Interpretação adotada** (a confirmar com o orientador): um *select* que transforma o
labirinto inteiro no valor calculado escolhido. Todas as células ficam coloridas por esse
valor e mostram o número quando ele cabe. Substitui os três botões da v0.3.1 e amplia o que
eles faziam.

| Opção | O que todas as células mostram |
|---|---|
| Mapa de calor e setas | V(s) em cores e a melhor ação em setas (visão padrão) |
| V(s): valor do estado | o maior Q de cada estado |
| Q(s, a): as 4 ações | os quatro valores em cruz, com a melhor sublinhada |
| Q(s, ↑) / Q(s, →) / Q(s, ↓) / Q(s, ←) | o valor de **uma** ação em todos os estados |
| Visitas | quantas vezes o agente passou por cada estado (escala de cor logarítmica) |

- Nas grades grandes, onde os números não cabem, **as cores continuam mostrando o valor
  escolhido** e a página sugere o inspetor.
- O caminho final passa a ser uma **borda verde** quando um valor está selecionado; antes, o
  verde cobria as células e escondia os valores.
- A legenda do mapa de calor muda conforme a opção, e o inspetor da célula ganhou a
  contagem de visitas.
- Os atalhos de teclado são ignorados enquanto o *select* está em foco.
- **Testes:** 21 no total, todos passando. No navegador real (Edge), os 8 modos foram
  verificados, junto com a legenda, o aviso em 41 × 41, o inspetor com visitas e os
  atalhos; nenhum erro de JavaScript.

## Parte 2 · Discussão no TCC

- Pesquisa bibliográfica com verificação de cada referência na fonte original (detalhes em
  [10-discussao-resultados.md](../10-discussao-resultados.md#verificação-das-referências)).
- Texto da seção **4.1 Discussão**, com quatro parágrafos:
  1. objetos de aprendizagem e engajamento (Wiley; Hundhausen, Douglas e Stasko; Naps *et al.*;
     Smilkov *et al.*), com os resultados Dijkstra × Backtracking;
  2. comparação com ferramentas para algoritmos clássicos (VisuAlgo; Lourenço *et al.*);
  3. comparação com ferramentas de Q-Learning (QUBE; Q-Learning Lab), com os resultados do γ;
  4. limitações (ausência de avaliação com estudantes) e trabalho futuro.
- Inserido no .docx do TCC (versão do Drive de 27/11, 16:22), com a formatação do próprio
  documento, e 8 referências novas no padrão já usado na lista. O arquivo passou na validação
  do formato.
- **Não citado:** o artigo do TBC-Grafos (ICECE 2007), porque o arquivo não pôde ser lido para
  conferência.

## Revisão da equipe
- Aceito:
- Alterado:
- Rejeitado:

## Evidências
- Capturas: `docs/img/v0.4-visualizar-visits.png`, `docs/img/v0.4-visualizar-left.png`, `docs/img/v0.4-visualizar-41x41-up.png`
- Arquivo do TCC: `TCC_Arielce_Rafael_discussao.docx` (na pasta do TCC, fora do repositório)
- Commit / deploy: *(preencher após a publicação)*
