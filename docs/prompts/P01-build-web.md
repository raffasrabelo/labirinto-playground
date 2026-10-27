# P01 · Build web com pygbag

| Campo | Valor |
|---|---|
| Data | 27/10/2026 |
| Sprint | S0 (adiantado da S1, a pedido da equipe, para a Review de 28/10) |
| Item(ns) do backlog | US-06, US-08 · Risco R1 |
| Autor do prompt | Rafael |
| Ferramenta / modelo | Claude Code (Claude Opus 5.5) |

## Prompt enviado

```text
Sim, tente o build web com pygbag agora (prompt P01) para eu levar o link na review de amanhã.
```

O pedido curto remete ao P01 do [catálogo](catalogo.md), que contém papel, contexto, tarefa,
restrições e critérios de aceite completos.

## Resultado obtido
- Build gerado com `pygbag 0.9.3` (pacote final de ~60 KB em `app/build/web/`; o Python
  3.12 e o pygame-ce 2.5.7 em WebAssembly vêm do CDN do pygbag).
- **Nenhuma alteração de código foi necessária.** O laço `async` de `main.py` e a fonte padrão
  do Pygame já eram compatíveis, porque a arquitetura foi pensada para o pygbag desde a S0.
- Testado no navegador: geração, sliders, seleção de algoritmo, pincel, Executar/Pausar/Continuar,
  Dijkstra e Backtracking. Os resultados são idênticos aos do desktop (semente 42, 21×21:
  Backtracking com custo 132, 64 passos e 71 células expandidas).

### Desempenho medido no navegador (tempo de atualização + desenho por quadro)

| Grade | Situação | Mediana | p95 |
|---|---|---|---|
| 21×21 | parado / executando a 100 passos/s | 5,5–6,7 ms | ≤ 10,7 ms |
| 61×61 | executando a 1000 passos/s | 9,5–10,6 ms | ≤ 17,0 ms |

O orçamento para 60 fps é de 16,7 ms por quadro, então **não é preciso limitar o tamanho da
grade na versão web** (RNF02 atendido). Medição feita em um único computador (o notebook de
desenvolvimento); em máquinas mais fracas, o primeiro ajuste seria o T-03 (redesenhar só as
células alteradas).

## Revisão da equipe
- Aceito:
- Alterado:
- Rejeitado:

## Problemas encontrados no caminho (úteis para o TCC)
1. **Servidor estático em `localhost` não funciona:** em `localhost`, o pygbag tenta baixar o
   pygame-ce de `/cdn/` no próprio servidor (erro 404). Para testar localmente é preciso usar o
   servidor do pygbag (`python -m pygbag app`), que redireciona ao CDN. Em hospedagem pública
   (GitHub Pages, itch.io) o problema não ocorre.
2. **Aba em segundo plano:** com a aba do navegador oculta, o navegador reduz a taxa de quadros
   e os cliques ficam enfileirados, o que parecia um bug sem ser. A medição só vale com a página visível.

## Evidências
- Commit / tag: *(pendente: repositório ainda não criado)*
- Testes: `pytest` ✅ (6/6) · teste de interação desktop ✅ · teste manual no navegador ✅
