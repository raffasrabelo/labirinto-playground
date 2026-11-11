# P04 · Implementação do Q-Learning (v0.3)

| Campo | Valor |
|---|---|
| Data | 11/11/2026 |
| Sprint | S3 (entregue antes do fim da sprint) |
| Item(ns) do backlog | US-16 a US-20, US-26 · RF13 a RF15 |
| Autor do prompt | Rafael |
| Ferramenta / modelo | Claude Code (Claude Opus 5.5) |
| Prompts de origem no catálogo | C08 (motor) e C09 (visualização) |

## Prompt enviado

```text
Vamos começar a implementação do Q-Learning e quero saber se o projeto já está hospedado
também para poderem utilizar pelo navegador. Meu professor orientador quer utilizar a
implementação de q-learning na aula de amanhã e assim poderemos também documentar o case
no TCC.
```

## Resultado obtido
- **Motor** `algorithms/qlearning.py`: Q-Learning tabular como gerador de eventos (`agent`,
  `episode`, `path`, `done`/`fail`), ε-greedy com decaimento, reprodutível pela semente.
- **Sessão:** parâmetros α, γ, ε, decaimento, episódios, recompensa no objetivo e penalidade
  na parede, todos validados. Velocidade máxima elevada para 100.000 passos/s, com limite de
  ~12 ms de processamento por quadro para a página não travar.
- **Labirinto (Pygame):** mapa de calor violeta do valor aprendido, setas da melhor ação e
  agente como um círculo laranja.
- **Página (HTML/CSS/JS):** painel de parâmetros com explicações curtas, botão "Restaurar
  valores padrão", métricas do treino e gráfico SVG de recompensa por episódio com média móvel.
- **Testes:** 4 do motor e 2 da sessão (18 no total, todos passando).
- **Roteiro de aula** [09-roteiro-aula-qlearning.md](../09-roteiro-aula-qlearning.md), com
  experimentos cujos resultados foram verificados um a um.

## Decisões tomadas com base em experimentos
1. **γ padrão = 0,995.** Com γ = 0,95 o agente não aprendeu nenhum dos 8 labirintos 21 × 21
   testados. Com 0,99, falhava em 3 de 8 labirintos 21 × 21 com 40% de lama. A análise
   mostrou que o agente chegava ao objetivo no início do treino e depois "desaprendia":
   passava a rodar em regiões pouco exploradas. Com 0,995, 7 de 8 passaram e nenhum cenário
   piorou (tabela em [06-algoritmos.md](../06-algoritmos.md#q-learning-escolha-dos-valores-padrão)).
2. **Previsões do roteiro corrigidas antes da aula.** A primeira versão do roteiro dizia que
   α = 0,05 só "demora mais" e que a lama a 40% seria contornada em qualquer grade. Os testes
   mostraram que, com 200 episódios, α = 0,05 não aprende, e o roteiro passou a indicar 500
   episódios. Também revelaram um resultado didático: com ε = 1 e sem decaimento, o caminho
   ótimo ainda é aprendido em 11 × 11 (Q-Learning é *off-policy*).

## Validação
- `pytest`: 18/18 ✅
- Navegador real (Edge, via Playwright): treino completo do labirinto 21 × 21 da demo
  (48.761 eventos) em menos de 1 s na velocidade máxima; caminho aprendido com custo 120,
  igual ao Dijkstra; com γ = 0,95 o status mostra "O agente não aprendeu o caminho".
- Dijkstra e Backtracking continuam com os mesmos resultados de antes.

## Revisão da equipe
- Aceito:
- Alterado:
- Rejeitado:

## Evidências
- Commit / deploy: *(preencher após a publicação)*
- Capturas: `docs/img/v0.3-qlearning-*.png` (legendas em [08](../08-legendas-das-figuras.md))
