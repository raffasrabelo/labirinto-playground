# P06 · Layout de aplicativo: labirinto sempre visível (v0.3.2)

| Campo | Valor |
|---|---|
| Data | 18/11/2026 |
| Sprint | S3 |
| Item(ns) do backlog | US-28 · RNF08 |
| Autor do prompt | Rafael |
| Ferramenta / modelo | Claude Code (Claude Opus 5.5) |

## Prompt enviado

```text
queria saber se conseguimos melhorar a disposição dos elementos na tela, visto que o
pygame fica no começo da pagina e as colunas laterais passam muito dele
```

## Diagnóstico (medido antes da mudança, no site publicado, com o Q-Learning selecionado)

| Tela | Altura da página | Coluna esquerda | Labirinto | Inspetor da tabela Q |
|---|---|---|---|---|
| 1366 × 768 | 1.875 px | 1.603 px | 482 px | começa em 781 px (**fora da tela**) |
| 1440 × 900 | 1.875 px | 1.603 px | 614 px | visível |
| 1920 × 1080 | 1.875 px | 1.603 px | 734 px | visível |
| 1024 × 768 | 3.273 px | 1.657 px | 482 px | em 2.640 px |

As colunas laterais cresceram com o Q-Learning (parâmetros, métricas, gráfico, inspetor),
enquanto o labirinto tinha altura limitada. Para ver os controles, era preciso rolar a
página, e o labirinto saía da tela.

## Resultado obtido (ADR-03)
- **Modo "aplicativo"** (largura ≥ 1181 px e altura ≥ 640 px): a página cabe exatamente na
  janela. O labirinto fica fixo no centro, com o maior tamanho que a coluna permite (calculado
  com *container queries* do CSS), e cada coluna lateral rola por dentro, com **sombras de
  rolagem** que indicam se há mais conteúdo acima ou abaixo.
- **Barra única:** título e controles de execução numa só linha, liberando altura para o
  labirinto; o link "código-fonte" foi para o rodapé.
- **Inspetor antes do gráfico** no painel de resultados, por ser usado junto com o mouse
  sobre o labirinto.
- **"Atalhos de teclado" recolhível**.
- **Telas intermediárias** (largura 761–1180 px ou altura < 640 px): o labirinto fica
  "grudado" no topo enquanto se rolam os controles.
- **Celular:** sem mudança (labirinto primeiro, uma coluna).
- Colunas laterais de 320 px em telas a partir de 1600 px de largura.

## Depois (mesmas medições)

| Tela | Altura da página | Labirinto | Inspetor da tabela Q |
|---|---|---|---|
| 1366 × 768 | **768 px (sem rolagem)** | **521 px** | visível (481–663 px) |
| 1440 × 900 | **900 px (sem rolagem)** | **653 px** | visível |
| 1920 × 1080 | **1.080 px (sem rolagem)** | **833 px** | visível |

O teste funcional completo (treino, valores Q, inspetor com mouse real, avisos) foi repetido
após a mudança, com os mesmos resultados e nenhum erro de JavaScript.

## Revisão da equipe
- Aceito:
- Alterado:
- Rejeitado:

## Evidências
- Capturas: `docs/img/layout-antes-1366x768.png` e `docs/img/layout-depois-1366x768.png`
- Commit / deploy: *(preencher após a publicação)*
