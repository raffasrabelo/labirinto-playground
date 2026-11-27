# P08 · Correção do interruptor (v0.4.1) e figuras da v0.3–v0.4 no TCC

| Campo | Valor |
|---|---|
| Data | 27/11/2026 |
| Sprint | S4 |
| Item(ns) do backlog | BUG-01 (interruptor), T-08 (figuras do TCC) |
| Autor do prompt | Rafael |
| Ferramenta / modelo | Claude Code (Claude Opus 5.5) |

## Prompt enviado

```text
coloque as legendas das novas figuras no TCC. Encontrei um bug quando clico na chavinha do
"Mostrar setas da política" que faz a tela quebrar na metade e não volta a não ser que atualize
```

## Parte 1 · Bug do interruptor (BUG-01)

**Reprodução (site publicado, v0.4, Edge):** ao clicar em "Mostrar setas da política", a
página inteira rolava: 771 px em tela de 1366 × 768 e 423 px em 1920 × 1080. A barra
superior e metade do labirinto saíam da tela. Como o modo aplicativo desliga a rolagem da
página (`overflow: hidden`), não havia como voltar sem recarregar. "Mostrar distâncias", no
Dijkstra, tinha o mesmo defeito.

**Causa:** a caixa de seleção real fica invisível dentro do interruptor, com
`position: absolute`. Como o interruptor não era um elemento posicionado, ela era
posicionada em relação à página, longe do interruptor. Ao clicar, o navegador dá foco à
caixa e rola a página até ela. Essa rolagem programática acontece mesmo com
`overflow: hidden`.

**Correção (v0.4.1):**
- `web/src/style.css`: `.switch` ganhou `position: relative`, e a caixa invisível passou a
  ter 1 × 1 px no canto do próprio interruptor;
- `web/src/app.js`: proteção extra. No modo aplicativo, se algo rolar a página, ela volta
  ao topo.

**Verificação (local, Edge):**
- Os dois interruptores foram testados em 4 tamanhos de tela (1366 × 768, 1920 × 1080,
  1024 × 768 e 390 × 844), com clique duplo (liga e desliga) e foco pelo teclado (Tab).
- No modo aplicativo a página não rolou nenhuma vez, **mesmo com a proteção do JavaScript
  desligada**: a causa foi eliminada no CSS.
- Nenhum erro de JavaScript.
- Observação: com foco no interruptor, o Espaço continua sendo o atalho de executar/pausar,
  como nos botões. Isso é comportamento definido, não defeito.

## Parte 2 · Figuras novas no TCC (T-08)

O documento do Drive (versão de 27/11, 16:22 UTC) não tinha figuras sem legenda. As
"figuras novas" eram as 10 capturas da v0.3 à v0.4, que ainda não estavam no TCC. Elas
foram inseridas no fim do capítulo de Resultados, antes de "4.1 Discussão":

| Figura no TCC | Captura | Legenda (docs/08) |
|---|---|---|
| 9 | v0.3-qlearning-treinando | A9 |
| 10 | v0.3-qlearning-concluido | A10 |
| 11 | v0.3-qlearning-gama-095 | A11 |
| 12 | v0.3-qlearning-valores-4-acoes | A12 |
| 13 | v0.3-qlearning-valores-melhor | A13 |
| 14 | layout-antes-1366x768 | A14 |
| 15 | layout-depois-1366x768 | A14 |
| 16 | v0.4-visualizar-visits | A15 |
| 17 | v0.4-visualizar-left | A15 |
| 18 | v0.4-visualizar-41x41-up | A15 |

- **Padrão ABNT (NBR 14724), igual ao das Figuras 1–8:** legenda acima ("Figura N – título",
  10 pt, centralizada), imagem centralizada e "Fonte: Elaborado pelos autores (2026)." abaixo.
- **Chamada no texto:** quatro parágrafos novos citam cada figura antes de ela aparecer (Q-Learning,
  valores da tabela Q, layout e seletor da v0.4).
- **Lista de Figuras:** entradas 9 a 18 acrescentadas, com a página "XX" destacada em
  amarelo, como as demais, para preencher na diagramação final.
- **Imagens:** reduzidas para 1.600 px de largura (≈ 250 dpi no tamanho impresso). A largura
  máxima é de 16 cm e a altura máxima de 17 cm, para que cada figura caiba na página com a
  legenda e a fonte.
- **Validação:** o validador do formato .docx aprovou o arquivo (407 → 451 parágrafos), e os
  comentários do documento foram preservados.

## Revisão da equipe
- Aceito:
- Alterado:
- Rejeitado:

## Evidências
- Arquivo do TCC: `TCC_Arielce_Rafael_figuras-v0.3-v0.4.docx` (na pasta do TCC, fora do repositório)
- Commit e deploy: *(preencher após a publicação)*
