# P03 · Interface híbrida: HTML/CSS + labirinto em Pygame

| Campo | Valor |
|---|---|
| Data | 27/10/2026 |
| Sprint | S0 |
| Item(ns) do backlog | T-05, RNF08 |
| Autor do prompt | Rafael |
| Ferramenta / modelo | Claude Code (Claude Opus 5.5) |
| Prompt de origem no catálogo | — (surgiu da análise da v0.1) |

## Contexto
Depois da publicação da v0.1, a equipe avaliou que os algoritmos funcionavam, mas o design
estava ruim. Foi feita uma pergunta de diagnóstico, que não está registrada como prompt de
execução: *"O que explica isso? E como podemos contornar?"*. A IA apontou três causas:
1. o Pygame não tem componentes de interface e só tem uma fonte disponível no navegador
   (FreeSansBold, toda em negrito);
2. o pygbag estica uma imagem fixa de 1280×760, deixando o texto borrado;
3. não houve etapa de design.

Foram apresentadas três opções (A: polir no Pygame; B: híbrido; C: web completa com Pyodide).

## Prompt enviado

```text
Vamos com a opção B. É o que eu estava pensando. Fazemos apenas a parte visual do
labirinto no pygame e todo o restante (configurações e design) em html/css
(e typescript se necessário).
```

## Resultado obtido
- **Python reorganizado:**
  - a lógica de estado saiu da interface e foi para `core/session.py` (Python puro, testável);
  - o Pygame ficou só com `ui/board.py` (desenho do labirinto e edição com o mouse);
  - `ui/playground.py` e `ui/widgets.py` foram removidos.
- **Ponte JSON JS↔Python** em `main.py` (`WebBridge`): a página enfileira comandos e o Python
  lê a fila a cada quadro (`pull`) e devolve o estado quando ele muda (`push`). Protocolo em
  [02-arquitetura.md](../02-arquitetura.md#ponte-javascript--python).
- **Interface web** em `web/src/`:
  - `template.html`: template próprio do pygbag, com estrutura da página e tela de carregamento;
  - `style.css`: design system com tokens de cor iguais aos do labirinto, fonte Inter,
    layout responsivo e o labirinto primeiro no celular;
  - `app.js`: controles, atalhos de teclado e envio do tamanho real do quadro.
- **Labirinto nítido:** o canvas é desenhado na resolução física da tela (CSS ×
  `devicePixelRatio`, até 2×) e se redimensiona com a janela.
- **`tools/build_web.py`**: junta HTML+CSS+JS no template e chama o pygbag. O CI passou a usá-lo.
- **Decisão sobre TypeScript:** não adotado por ora. A página tem ~200 linhas e assim dispensa
  Node.js e uma etapa de compilação. Fica registrado como opção se a interface crescer (ADR-02).
- **Modo desktop** mantido como ferramenta de desenvolvimento: só o labirinto e atalhos de teclado.
- **Testes:** 6 novos testes da sessão, com 12 no total, todos passando sem Pygame instalado.

## Validação no navegador
- Carregamento, ponte, títulos e métricas: ✅
- Backtracking (semente 42, 21×21): 71 células expandidas, 64 passos, custo 132, iguais à v0.1 ✅
- Sliders, semente, sorteio (G), Espaço, troca de algoritmo e de pincel: ✅
- Desenho com arraste de mouse real: uma linha de parede atravessando a grade faz o Dijkstra
  responder "Não existe caminho" ✅
- Celular (375 px): sem rolagem horizontal; canvas em 2× ✅

## Problemas encontrados no caminho (úteis para o TCC)
1. **Atalhos quebravam fora de elementos HTML:** `e.target.matches` não existe quando o evento
   vem do `document`. Corrigido com `instanceof Element`.
2. **Espaço com botão focado:** acionaria o atalho e o clique do botão ao mesmo tempo.
   Corrigido bloqueando o `keyup` do Espaço.
3. **Eventos de mouse sintéticos:** o SDL usa a última posição conhecida do mouse no evento de
   clique. Por isso, testes automatizados com eventos JavaScript simulados não reproduzem o
   arraste. O teste válido é com mouse real.

## Revisão da equipe
- Aceito:
- Alterado:
- Rejeitado:

## Evidências
- Commit: *(preencher)*
- Testes: `pytest` ✅ 12/12 · teste manual no navegador ✅
