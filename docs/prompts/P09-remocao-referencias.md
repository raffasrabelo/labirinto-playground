# P09 · Remoção de duas referências da discussão do TCC

| Campo | Valor |
|---|---|
| Data | 27/11/2026 |
| Sprint | S4 |
| Item(ns) do backlog | T-07 (discussão do TCC) |
| Autor do prompt | Rafael |
| Ferramenta / modelo | Claude Code (Claude Opus 5.5) |

## Prompt enviado

```text
Queremos retirar as referências de hundhausen e do myers e adequar o texto sem elas. mantenha
o trecho que explica o experimento que definiu o γ padrão em 0,995.
```

## Resultado obtido

Removidas a pedido da equipe: **Hundhausen, Douglas e Stasko (2002)** e **Myers, Xie e Zhu
(2020)** (QUBE). O texto da seção 4.1 foi adequado assim:

| Parágrafo | Antes | Depois |
|---|---|---|
| 1 (objetos de aprendizagem) | Meta-estudo de Hundhausen *et al.* sustentava que "ter a visualização não basta"; Naps *et al.* vinham "na mesma direção" | A mesma ideia passa a ser sustentada só por Naps *et al.* (2003): pouco valor educacional sem aprendizagem ativa, mais a taxonomia de engajamento |
| 3 (ferramentas de Q-Learning) | QUBE (Myers *et al.*) + Q-Learning Lab | Só o Q-Learning Lab; **o trecho do experimento do γ (0,99 × 0,95 → padrão 0,995) ficou idêntico** |
| 4 (limitações) | "diferentemente do QUBE" e "como alertam Hundhausen *et al.*" | "assim como o Q-Learning Lab"; a ressalva passa a ser que os ganhos do engajamento ainda precisam ser confirmados na prática |

- **Parágrafo 2** (VisuAlgo e Lourenço *et al.*): sem mudança.
- **Referências:** as duas entradas e as linhas em branco que as separavam saíram da lista; a
  ordem alfabética das demais foi mantida.
- **Formatação:** os "et al." seguem em itálico.
- **Verificação automática:** nenhuma menção aos dois autores ou ao QUBE no documento, e o
  trecho do γ foi preservado.
- **Validação:** o validador do formato .docx aprovou o arquivo (451 → 447 parágrafos).
- `docs/10-discussao-resultados.md` foi atualizado da mesma forma.

## Revisão da equipe
- Aceito:
- Alterado:
- Rejeitado:

## Evidências
- Arquivo do TCC: `TCC_Arielce_Rafael_sem-hundhausen-myers.docx` (na pasta do TCC, fora do repositório),
  gerado a partir de `TCC_Arielce_Rafael_figuras-v0.3-v0.4.docx`
