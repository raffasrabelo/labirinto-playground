# P12 · Figuras só da versão atual e manual de uso (Apêndice A)

| Campo | Valor |
|---|---|
| Data | 27/11/2026 |
| Sprint | S4 |
| Item(ns) do backlog | T-10 (figuras), T-11 (manual) |
| Autor do prompt | Rafael |
| Ferramenta / modelo | Claude Code (Claude Opus 5.5) |

## Prompt enviado

```text
Agora quero que você retire as imagens das versões anteriores. Atualize e deixe apenas as imagens
da versão atual da aplicação. Junto a isso, em Apêndices, coloque um tutorial da aplicação mostrando
como devem ser utilizados todos os parâmetros, separado por algoritmos. Isso será o manual de uso da
aplicação.
```

## Parte 1 · Figuras da versão atual (Resultados)

- **Capturas novas:** 12 capturas da v0.4.1 feitas no site publicado (Edge, 1440 × 900, 2×), com
  as mesmas situações das figuras antigas. Os números do texto vêm das métricas registradas em
  cada captura.
- **Figuras removidas:** as 17 de versões anteriores (v0.1 a v0.4), junto com os arquivos de
  imagem sem uso dentro do .docx. A Figura 1 (Scrum) não é captura da aplicação e foi mantida.
- **Texto reescrito para contar a evolução sem as imagens antigas:**
  - o 1º parágrafo (dos autores) explica por que a v0.1 era insatisfatória, com o diagnóstico
    registrado no P03, em vez de remeter às Figuras 2–4;
  - um parágrafo novo resume as versões 0.2 a 0.4.1 e traz o **link do site publicado** e do
    **repositório**, atendendo ao comentário do orientador nesse trecho ("Adicionar prints da
    aplicação, e ir mostrando o que foi feito. Disponibilizar os links dos repositórios e
    deploys"). O comentário continua ancorado no trecho novo;
  - mais três parágrafos apresentam as Figuras 2–5 (Dijkstra, Backtracking, celular), 6–8
    (Q-Learning e o efeito do γ) e 9–13 (seletor "Visualizar no labirinto").
- **Números conferidos nas capturas:**

  | Execução | Medido |
  |---|---|
  | Dijkstra 21 × 21, semente 42 | 232 células expandidas, 56 passos, custo 120 |
  | Backtracking 41 × 41 | caminho de 168 passos, custo 316, pilha máxima de 169 |
  | Q-Learning 21 × 21 (padrão) | custo 120, 184 de 200 episódios chegaram ao objetivo |
  | Q-Learning com γ = 0,95 | não aprendeu (6 de 200 episódios chegaram) |
  | Q-Learning 41 × 41, 200 episódios | não aprendeu, coerente com a ressalva da seção 4.1 |

- **Lista de Figuras:** refeita com as Figuras 2 a 15.

## Parte 2 · Manual de uso (Apêndice A)

- **Título:** "APÊNDICE I" virou **"APÊNDICE A – MANUAL DE USO DO LABIRINTO PLAYGROUND"**.
  Pela NBR 14724, apêndices são identificados por letras maiúsculas.
- **Página:** o apêndice passou a começar em página nova por quebra de página, no lugar das 20
  linhas em branco que havia antes.
- **Seções:**
  - A.1 Acesso;
  - A.2 Visão geral da interface (Figura 14, com as áreas numeradas, e Figura 15, com os três
    painéis);
  - A.3 Execução e atalhos;
  - A.4 Parâmetros do labirinto;
  - A.5 Backtracking;
  - A.6 Dijkstra;
  - A.7 Q-Learning.
- **Conteúdo de cada parâmetro:** faixa, padrão e efeito, conferidos no código
  (`template.html`, `session.py`, `maze.py`, `qlearning.py`). Cada algoritmo tem também uma
  sugestão de atividade.
- **No repositório:** a mesma versão está em [11-manual-de-uso.md](../11-manual-de-uso.md).

## Verificações
- Validador do formato .docx aprovou o arquivo; figuras 1 a 15 em sequência, cada uma citada no
  texto antes de aparecer.
- Comentário do orientador nos Resultados: ancorado do novo parágrafo da evolução até a fonte da
  Figura 5.
- Nenhum erro de JavaScript durante as capturas.

## Pendências para a equipe
- **Diagramação:** o .docx não pôde ser aberto num editor aqui (não há Word nem LibreOffice
  instalados). Confira a diagramação ao abrir.
- **Páginas:** preencha as páginas da Lista de Figuras ("XX") e atualize o Sumário.
- **Comentário do orientador na Figura 1:** "Remover esse diagrama e inserir dos módulos da
  aplicação". Não fazia parte deste pedido.

## Revisão da equipe
- Aceito:
- Alterado:
- Rejeitado:

## Evidências
- Arquivo do TCC: `TCC_Arielce_Rafael_v0.4.1-manual.docx` (na pasta do TCC, fora do repositório),
  gerado a partir de `TCC_Arielce_Rafael_revisado.docx`
- Capturas: `docs/img/v0.4.1-*.png`
