# P11 · Tamanhos de labirinto na discussão e coerência da seção 3.1

| Campo | Valor |
|---|---|
| Data | 27/11/2026 |
| Sprint | S4 |
| Item(ns) do backlog | T-07 (discussão), T-09 (metodologia) |
| Autor do prompt | Rafael |
| Ferramenta / modelo | Claude Code (Claude Opus 5.5) |

## Prompt enviado

```text
corrija também o "11 × 11 a 31 × 31" na discussão. Confira os dois primeiros parágrafos do
item 3.1. Eles são contraditórios ao dizer sobre a natureza do trabalho ser "pesquisa aplicada"
e logo depois dizer que é pesquisa exploratória? Todas essas classificações que citamos são
contraditórias de alguma maneira?
```

## Parte 1 · Tamanhos de labirinto (seção 4.1)

- **Origem do "31 × 31":** eram os tamanhos testados no experimento do γ
  ([06-algoritmos.md](../06-algoritmos.md)). A plataforma, porém, aceita de 11 × 11 a 61 × 61
  (`app/core/session.py`).
- **Correção:** "de 11 × 11 a 61 × 61 células". Uma frase nova, depois do trecho do γ (que não
  mudou), informa que grades maiores exigem mais episódios. Em 31 × 31, com os valores padrão,
  o caminho ótimo saiu em 1 de 8 casos com 200 episódios e em 4 de 4 com 500. Sem essa
  ressalva, o texto sugeriria que o treino padrão funciona em qualquer tamanho.
- **Ajuste ligado à correção:** "nos 16 labirintos testados" virou "nos 16 labirintos de
  11 × 11 e 21 × 21 com 15% de lama". São exatamente os casos da tabela de γ = 0,99. Sem a
  especificação, a frase sobre o 31 × 31 parecia contradizer o total de 16.

## Parte 2 · As classificações da seção 3.1 são contraditórias?

**Não.** Cada uma responde a um critério diferente, e um trabalho recebe uma classificação em
cada critério:

| Critério | Classificação no TCC | Base em Gil (2002) |
|---|---|---|
| Natureza (por que se pesquisa) | Aplicada | p. 17: razões "de ordem prática"; o autor diz que pesquisa pura e aplicada não são mutuamente exclusivas |
| Objetivos | Exploratória | p. 41: proporcionar familiaridade com o problema, torná-lo explícito ou constituir hipóteses |
| Procedimentos (delineamento) | Pesquisa bibliográfica + estudo de caso | p. 41 e 43: a exploratória costuma assumir exatamente essas duas formas |
| Abordagem | Predominantemente qualitativa | — (os números da plataforma entram como complemento) |

**Pontos de atenção (não são contradições):**
- **Sem citação:** a frase "pesquisa aplicada" não cita fonte. Pode citar Gil (2002, p. 17),
  já presente nas referências.
- **Qualitativa com números:** a plataforma gera dados numéricos, como custo e células
  expandidas. "Predominantemente" e "complementadas" deixam isso coerente, porque os números
  servem para verificar a plataforma, não para medir aprendizagem.
- **Coerência com a discussão:** "exploratória" combina com a limitação declarada na
  discussão (ainda não houve avaliação com estudantes). Gil (2002, p. 54) observa que os
  resultados de estudos de caso costumam ser apresentados como hipóteses, não como conclusões.

## Parte 3 · Citação de Gil na "pesquisa aplicada" (aprovada pela equipe)

Prompt de continuação: `Sim, citar`. A frase passou a ser: "Quanto à sua natureza, trata-se
de uma pesquisa aplicada, isto é, motivada por razões de ordem prática (GIL, 2002, p. 17), uma
vez que busca gerar conhecimentos para a solução de um problema prático e específico [...]".
A expressão "razões de ordem prática" é a usada por Gil na p. 17. A referência já constava da
lista.

## Revisão da equipe
- Aceito:
- Alterado:
- Rejeitado:

## Evidências
- Arquivo do TCC: `TCC_Arielce_Rafael_revisado.docx` (na pasta do TCC, fora do repositório),
  gerado a partir de `TCC_Arielce_Rafael_metodologia.docx`; aprovado pelo validador do formato .docx.
