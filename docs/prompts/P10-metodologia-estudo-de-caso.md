# P10 · Seção 3.1: classificação da pesquisa e estudo de caso

| Campo | Valor |
|---|---|
| Data | 27/11/2026 |
| Sprint | S4 |
| Item(ns) do backlog | T-09 (metodologia do TCC) |
| Autor do prompt | Rafael |
| Ferramenta / modelo | Claude Code (Claude Opus 5.5) |

## Prompt enviado

```text
adapte o seguinte trecho para se encaixar com a metodologia adotada no nosso trabalho:

3.1 Metodologia Adotada
Com o objetivo de resolver um problema aplicado através da utilização de tecnologia, o método
de pesquisa utilizado no trabalho foi o um estudo de caso com método de dados de natureza
qualitativa. Ventura (2007, p.384) diz em sua obra: [citação longa] (VENTURA, 2007, p.384).
https://files.cercomp.ufg.br/weby/up/150/o/Anexo_C1_como_elaborar_projeto_de_pesquisa_-_antonio_carlos_gil.pdf
```

## Problemas no trecho original
- Estava quebrado em uma linha por parágrafo (colado de PDF).
- Repetia a autoria da citação: "Ventura (2007, p.384) diz" e, no fim, "(VENTURA, 2007, p.384)".
- Tinha erro de digitação ("foi o um estudo de caso") e o link do Gil solto no texto.
- Repetia a classificação "aplicada", que o parágrafo seguinte já fazia.
- Não dizia qual é o caso estudado nem de onde vêm os dados.

## Resultado obtido
A seção 3.1 agora segue a classificação de Gil (2002): natureza (aplicada, parágrafo já
existente), objetivos (exploratória) e procedimentos (pesquisa bibliográfica e estudo de caso).

1. **Objetivos:** pesquisa exploratória, com citação direta curta de Gil (2002, p. 41). Na
   p. 41, Gil diz que esse tipo de pesquisa costuma assumir a forma de pesquisa bibliográfica
   ou de estudo de caso, os dois procedimentos deste trabalho.
2. **Estudo de caso:** definição de Gil (2002, p. 54), seguida da citação longa de Ventura
   (2007, p. 384) no formato da NBR 10520: recuo de 4 cm, fonte 10, espaçamento simples, sem
   aspas.
3. **O caso:** o desenvolvimento e a utilização do Labirinto Playground (IFSULDEMINAS, Campus
   Machado, 2026). A abordagem é predominantemente qualitativa, com estas fontes de dados:
   - validações com o orientador nas Sprint Reviews;
   - sugestões dele após a aula de Q-Learning;
   - registros de desenvolvimento (backlog, versões, prompts);
   - medições da plataforma (custo dos caminhos, células expandidas), como complemento.
4. **Referências:** Gil (2002) e Ventura (2007) acrescentadas no padrão da lista. O link solto
   saiu do texto.

## Verificação das fontes

| Fonte | Como foi conferida | Observação |
|---|---|---|
| GIL, A. C. *Como elaborar projetos de pesquisa*. 4. ed. São Paulo: Atlas, 2002 | Folha de rosto, ficha catalográfica e p. 41 e 54 do PDF indicado (páginas digitalizadas lidas como imagem) | As duas citações diretas conferem com o texto impresso |
| VENTURA, M. M. O estudo de caso como modalidade de pesquisa. *Revista SOCERJ*, v. 20, n. 5, p. 383-386, 2007 | Dados da referência e p. 384 confirmados em trabalhos que citam o artigo | **O artigo original não abriu** (o site da revista recusou a conexão). A redação da citação longa é a que já estava no TCC; confira no original |

## Revisão da equipe
- Aceito:
- Alterado:
- Rejeitado:

## Evidências
- Arquivo do TCC: `TCC_Arielce_Rafael_metodologia.docx` (na pasta do TCC, fora do repositório),
  gerado a partir de `TCC_Arielce_Rafael_sem-hundhausen-myers.docx`. O validador do formato
  .docx aprovou o arquivo (447 → 442 parágrafos).
