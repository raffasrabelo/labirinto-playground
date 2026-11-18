# P05 · Valores da tabela Q no labirinto e inspetor de célula (v0.3.1)

| Campo | Valor |
|---|---|
| Data | 18/11/2026 |
| Sprint | S3 |
| Item(ns) do backlog | US-27 |
| Autor do prompt | Rafael |
| Origem | **Sugestão do orientador** após o uso da plataforma em aula |
| Ferramenta / modelo | Claude Code (Claude Opus 5.5) |

## Prompt enviado

```text
o professor sugeriu colocar uma opção de mostrar os valores de cada posição dos estados
(posições) do q-table
```

## Resultado obtido
- **Opção "Valores da tabela Q no labirinto"** (seção Exibição, só no Q-Learning):
  - **Nenhum:** só o mapa de calor e as setas, como antes;
  - **Melhor:** o maior Q de cada célula, no centro; a seta da política vira um triângulo
    pequeno junto à borda;
  - **4 ações:** Q(↑), Q(→), Q(↓) e Q(←) em cruz dentro da célula, com a melhor ação em
    negrito e sublinhada (as setas ficam ocultas, pois o sublinhado já indica a ação).
- **Inspetor da tabela Q** (painel Resultado): mostra os 4 valores, com uma casa decimal, da
  célula sob o mouse ou, sem mouse (como no celular), da célula do agente. Também explica
  células de parede, o objetivo e células ainda não visitadas.
- **Legibilidade garantida pelo tamanho real na tela:** a página informa ao Python a
  densidade de pixels (`dpr`), e os números só são desenhados se a célula tiver pelo menos
  28 px de tela ("Melhor") ou 42 px ("4 ações"). Caso contrário, a página exibe um aviso e
  sugere o inspetor. Na prática: "4 ações" em grades 11 × 11 e 13 × 13; "Melhor" até ~21 × 21.
- Textos renderizados com cache, para não pesar durante o treino.
- **Testes:** 2 novos na sessão (20 no total, todos passando).

## Problemas encontrados no caminho
1. **Calibração da fonte:** os tamanhos foram definidos medindo a fonte padrão do Pygame
   (largura de "-12" ≈ 0,95 × tamanho), para que os 4 valores coubessem sem se sobrepor.
2. **Aviso que não sumia:** a regra CSS `.field small { display: block }` anulava o atributo
   `hidden`. Corrigido com a regra global `[hidden] { display: none !important; }`.
3. **Ambiente de testes temporário apagado** duas vezes durante a sessão (executáveis
   removidos da pasta temporária); foi recriado.

## Validação
- `pytest`: 20/20 ✅
- Navegador real (Edge, via Playwright, com movimento de mouse real):
  - 11 × 11 em "4 ações": números visíveis e sem aviso; o inspetor na célula (4, 2) mostrou
    ↑ 37,6 · ← 40,7 · **→ 54,5 (melhor)** · ↓ 38,4;
  - ao tirar o mouse do labirinto, o inspetor é limpo;
  - 21 × 21 em "4 ações": aviso exibido; em "Melhor": sem aviso, números visíveis;
  - nenhum erro de JavaScript.

## Revisão da equipe
- Aceito:
- Alterado:
- Rejeitado:

## Evidências
- Capturas: `docs/img/v0.3-qlearning-valores-4-acoes.png`, `docs/img/v0.3-qlearning-valores-melhor.png`
- Commit: `b734864` · deploy: <https://github.com/raffasrabelo/labirinto-playground/actions/runs/44417447532> (test, build e deploy ✅)
- Site público testado após o deploy (Edge, mouse real): rodapé v0.3.1; os mesmos resultados
  do teste local (inspetor, aviso em 21 × 21 no modo "4 ações", modo "Melhor" visível,
  nenhum erro de JavaScript).
