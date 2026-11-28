# P13 · Diagrama de módulos no lugar da Figura 1

| Campo | Valor |
|---|---|
| Data | 27/11/2026 |
| Sprint | S4 |
| Item(ns) do backlog | T-12 |
| Autor do prompt | Rafael |
| Ferramenta / modelo | Claude Code (Claude Opus 5.5) |

## Prompt enviado

```text
Sim, fazer
```

O prompt respondeu a uma pergunta feita ao fim do [P12](P12-figuras-atuais-e-manual.md): "Faço o
diagrama de módulos que o orientador pediu no lugar da Figura 1?". O orientador tinha deixado
este comentário na Figura 1 do TCC, o ciclo de sprint do Scrum: "Remover esse diagrama e inserir
dos módulos da aplicação".

## O que foi feito

- **Diagrama novo:** [modulos-da-aplicacao.svg](../img/modulos-da-aplicacao.svg) (fonte editável)
  e [modulos-da-aplicacao.png](../img/modulos-da-aplicacao.png) (3000 × 2520 px, inserido no TCC
  com 16 cm de largura). O conteúdo saiu dos `import` de cada arquivo do código. O diagrama mostra:
  - **Interface web** (`web/src/`): `template.html`, `style.css`, `app.js` e o canvas do
    labirinto.
  - **Aplicação Python** (`app/`, pygame-ce em WebAssembly pelo pygbag): `main.py` e as pastas
    `core/` (`session.py`, `grid.py`, `maze.py`, `run_state.py`), `algorithms/`
    (`backtracking.py`, `dijkstra.py`, `qlearning.py`, `base.py`) e `ui/` (`board.py`,
    `theme.py`).
  - **Ligações:**
    - entre `app.js` e `main.py`, a ponte JSON (comandos com `pull()`, estado com `push()`);
    - entre a sessão e os algoritmos, `next()` e os eventos;
    - `board.py` desenha no canvas, lê o estado da sessão e envia as edições.
  - **Fora do navegador:** `app/tests/` (pytest) e `tools/build_web.py`.
- **TCC** (`TCC_Arielce_Rafael_modulos.docx`):
  - a imagem do ciclo do Scrum saiu. A frase "A Figura 1 apresenta o ciclo de sprint adotado no
    projeto." também saiu, e o texto sobre o Scrum ficou como estava;
  - o diagrama de módulos virou a nova Figura 1, no fim da seção 3.1, depois de um parágrafo novo
    que apresenta os módulos e cita a figura;
  - **legenda:** "Figura 1 – Módulos do Labirinto Playground e comunicação entre eles", com a
    fonte "Elaborado pelos autores (2026)." A Lista de Figuras foi atualizada;
  - **comentário do orientador:** continua ancorado na imagem, agora a do diagrama novo, para ele
    conferir e resolver.
- **Documentação:**
  - [02 · Arquitetura](../02-arquitetura.md) (diagrama na seção "Visão em camadas");
  - [07 · Diagramas](../07-diagramas.md) (item 14a);
  - [08 · Legendas](../08-legendas-das-figuras.md) (D0 e nota do mapeamento no TCC);
  - [05 · Backlog](../05-backlog.md) (T-12).

## Verificações

- O validador do formato .docx aprovou o arquivo.
- A Figura 1 é citada no texto antes de aparecer e a numeração das Figuras 2 a 15 não mudou.
- O diagrama foi conferido visualmente: nenhum texto sobreposto e nenhuma seta cruzando rótulos.

## Pendências para a equipe

- **Diagramação:** conferir no Word ou no Google Docs. Aqui não há editor instalado para isso.
- **Página:** preencher a página da Figura 1 na Lista de Figuras.
- **Ciclo do Scrum:** se quiserem mantê-lo em algum lugar, ele continua no repositório, em
  [03 · Processo de trabalho](../03-processo-de-trabalho.md). Pode entrar, por exemplo, em um
  apêndice.

## Revisão da equipe
- Aceito:
- Alterado:
- Rejeitado:

## Evidências
- Arquivo do TCC: `TCC_Arielce_Rafael_modulos.docx` (na pasta do TCC, fora do repositório),
  gerado a partir de `TCC_Arielce_Rafael_v0.4.1-manual.docx`
- Diagrama: `docs/img/modulos-da-aplicacao.svg` e `.png`
