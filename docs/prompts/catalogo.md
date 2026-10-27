# Catálogo de Prompts Planejados (por sprint)

Prompts prontos para uso, já no formato padrão. Ajuste o bloco **CONTEXTO** com o
feedback recebido na Review anterior antes de enviar. Depois de usar, registre o
resultado em um arquivo `PXX-*.md` (ver [README](README.md)).

> Cabeçalho comum: todo prompt começa citando `docs/02-arquitetura.md` e
> `docs/05-backlog.md`, para a IA respeitar as decisões já tomadas.

---

## Sprint 1 · Web + Dijkstra completo

### P01 · Build web com pygbag (US-06, US-08) ← primeira tarefa da S1, maior risco técnico
```text
PAPEL: Atue como desenvolvedor sênior especialista em Python, pygame-ce e pygbag.
CONTEXTO: O app em app/ roda no desktop (python main.py). Leia docs/02-arquitetura.md.
Feedback da Review S0: <colar>.
TAREFA: Faça o app rodar no navegador com pygbag: gere o build, teste localmente,
identifique incompatibilidades (fontes, laço assíncrono, desempenho) e corrija.
Meça o FPS para grades 21, 41 e 61 e proponha o tamanho máximo na versão web.
RESTRIÇÕES: Não alterar a lógica em algorithms/ e core/. Os testes pytest devem continuar passando.
CRITÉRIOS DE ACEITE: build abre no Chrome/Edge/Firefox; todas as interações funcionam;
tabela de FPS documentada; instruções de build no README.
FORMATO DA SAÍDA: código alterado + seção "Versão web" no README + tabela de FPS.
```

### P02 · Publicação no GitHub Pages (US-07, T-02)
```text
PAPEL: Atue como engenheiro DevOps.
CONTEXTO: Repositório GitHub <url>. Build pygbag funcionando localmente (P01).
TAREFA: Crie um workflow do GitHub Actions que rode o pytest e, se passar, gere o
build pygbag e publique no GitHub Pages a cada push na main.
RESTRIÇÕES: Só usar ações oficiais do GitHub; nada de segredos além do GITHUB_TOKEN.
CRITÉRIOS DE ACEITE: o push na main atualiza o link público; um teste falhando bloqueia a publicação.
FORMATO DA SAÍDA: arquivo .github/workflows/*.yml + passo a passo de configuração.
```

### P03 · Pseudocódigo destacado + fila de prioridade (US-10, US-11)
```text
PAPEL: Atue como desenvolvedor full-stack sênior com experiência em ferramentas educacionais.
CONTEXTO: O Dijkstra emite eventos frontier/visit/path. Feedback da Review: <colar>.
TAREFA: Adicione um painel de pseudocódigo do Dijkstra cuja linha ativa fica destacada
conforme o evento atual, e um painel com as próximas 5 células da fila de prioridade
(célula e distância).
RESTRIÇÕES: Manter o padrão de geradores (o evento passa a informar a linha do
pseudocódigo em data["line"]); não quebrar os testes; layout deve caber em 1280x760.
CRITÉRIOS DE ACEITE: no modo Passo, cada clique avança uma linha coerente do pseudocódigo;
novos testes cobrindo data["line"].
FORMATO DA SAÍDA: código + testes + atualização de docs/02-arquitetura.md.
```

### P04 · Escrita: requisitos e arquitetura no Cap. 3
```text
PAPEL: Atue como orientador de TCC em Sistemas de Informação, especialista em normas ABNT.
CONTEXTO: docs/01-visao-e-requisitos.md e docs/02-arquitetura.md descrevem o sistema.
O capítulo 3 do TCC (Materiais e Métodos) já tem a seção 3.1 Metodologia (colar trecho).
TAREFA: Proponha as seções 3.2 Requisitos e 3.3 Arquitetura em linguagem acadêmica,
referenciando figuras (diagramas) e tabelas.
RESTRIÇÕES: Não inventar referências; marcar com [CITAR] onde faltar fonte; 3ª pessoa, impessoal.
CRITÉRIOS DE ACEITE: texto coerente com os documentos; numeração de figuras e tabelas.
FORMATO DA SAÍDA: texto pronto para colar no Word + lista de figuras a exportar.
```

---

## Sprint 2 · Backtracking completo

### P05 · Visualização da pilha de recursão (US-12, US-15)
```text
PAPEL: Atue como desenvolvedor sênior e professor de Estruturas de Dados.
CONTEXTO: backtracking.py simula a recursão com pilha explícita e emite visit/backtrack
com "depth". Feedback da Review S1: <colar>.
TAREFA: Crie um painel "Pilha de chamadas" mostrando os quadros (resolver(x,y)) empilhados,
com o topo destacado, e o pseudocódigo recursivo com a linha ativa.
RESTRIÇÕES: Pilhas grandes devem ser truncadas ("... +N quadros"); manter o FPS no navegador.
CRITÉRIOS DE ACEITE: ao retroceder, o quadro some da pilha em sincronia com a célula vermelha;
testes atualizados.
FORMATO DA SAÍDA: código + testes + captura de tela para o TCC.
```

### P06 · Ordem dos vizinhos e modo exaustivo (US-13, US-14)
```text
PAPEL: Atue como desenvolvedor sênior.
CONTEXTO: Backtracking com visualização de pilha pronto (P05).
TAREFA: (1) Parâmetro "ordem de exploração" (ex.: C-D-B-E, aleatória com semente).
(2) Modo "todas as soluções" que desmarca células ao retroceder e conta caminhos,
habilitado apenas para grades <= 11x11, com contador de soluções e melhor custo.
RESTRIÇÕES: Modo exaustivo deve poder ser interrompido a qualquer momento.
CRITÉRIOS DE ACEITE: testes provando que o melhor custo do modo exaustivo == custo do Dijkstra.
FORMATO DA SAÍDA: código + testes.
```

### P07 · Escrita: resultados de Dijkstra e Backtracking
```text
PAPEL: Atue como orientador de TCC.
CONTEXTO: Métricas coletadas: <colar tabela de experimentos: semente, tamanho, aberturas,
lama, células expandidas e custo para cada algoritmo>.
TAREFA: Redija a seção de Resultados comparando os dois algoritmos com base nos dados,
relacionando com a dificuldade de abstração citada no referencial (Vieira et al., 2015).
RESTRIÇÕES: Não extrapolar além dos dados; indicar onde inserir figuras.
FORMATO DA SAÍDA: texto + tabela formatada.
```

---

## Sprint 3 · Q-Learning

### P08 · Motor do Q-Learning (US-16, US-17)
```text
PAPEL: Atue como especialista em Aprendizado por Reforço e desenvolvedor Python sênior.
CONTEXTO: Desenho previsto em docs/02-arquitetura.md (seção Q-Learning). Leia algorithms/base.py.
TAREFA: Implemente algorithms/qlearning.py como gerador: estados = células, 4 ações,
recompensas configuráveis, epsilon-greedy com decaimento, emitindo eventos por passo
e por episódio (granularidade configurável).
RESTRIÇÕES: Python puro (sem numpy, para não pesar no navegador); reprodutível por semente.
CRITÉRIOS DE ACEITE: testes mostrando que, em labirinto 11x11 sem lama, a política gulosa
após N episódios chega ao objetivo; desempenho de >= 10 mil passos/s no desktop.
FORMATO DA SAÍDA: código + testes + parâmetros padrão recomendados (com justificativa).
```

### P09 · Visualização do Q-Learning (US-18, US-19, US-20)
```text
PAPEL: Atue como desenvolvedor full-stack sênior com foco em visualização de dados.
CONTEXTO: qlearning.py pronto (P08). Interface em ui/playground.py.
TAREFA: Sliders para alfa, gama, epsilon, decaimento, episódios; mapa de calor de max Q;
setas da melhor ação; mini-gráfico de recompensa por episódio; botão "Assistir agente".
RESTRIÇÕES: Painel de parâmetros muda conforme o algoritmo; caber em 1280x760; FPS >= 30 na web.
CRITÉRIOS DE ACEITE: aluno consegue ver a política "emergir" ao longo dos episódios.
FORMATO DA SAÍDA: código + capturas de tela.
```

---

## Sprint 4 · Validação e polimento

### P10 · Instrumento de validação com usuários (US-23)
```text
PAPEL: Atue como pesquisador em Informática na Educação.
CONTEXTO: Plataforma pronta; público: alunos do 1º ao 3º período. Restrições éticas
definidas com o orientador: <colar>.
TAREFA: Monte um roteiro de uso (tarefas guiadas de 15 min) e um questionário
(SUS + perguntas de percepção de aprendizagem em escala Likert + 2 abertas).
CRITÉRIOS DE ACEITE: aplicável em 20 min; perguntas ligadas à questão de pesquisa.
FORMATO DA SAÍDA: roteiro + questionário pronto para Google Forms + plano de análise.
```

### P11 · Revisão de qualidade e acessibilidade (US-21, US-24)
```text
PAPEL: Atue como revisor de código sênior e especialista em UX/acessibilidade.
TAREFA: Revise o código (bugs, legibilidade, desempenho) e a interface (contraste,
daltonismo, textos). Proponha e implemente um tutorial de 4 passos.
FORMATO DA SAÍDA: lista priorizada de problemas + correções aplicadas.
```

---

## Sprint 5 · Fechamento

### P12 · Resumo, Abstract e Conclusão
```text
PAPEL: Atue como orientador de TCC especialista em ABNT.
CONTEXTO: <colar objetivos, resultados e discussão finais>.
TAREFA: Redija o Resumo (150–500 palavras), o Abstract equivalente, as palavras-chave
e a Conclusão respondendo explicitamente à questão de pesquisa e a cada objetivo específico.
FORMATO DA SAÍDA: textos prontos para o Word.
```

### P13 · Roteiro da apresentação final
```text
PAPEL: Atue como especialista em apresentações acadêmicas.
TAREFA: Monte um roteiro de 15–20 min com sugestão de slides e uma demo ao vivo
(com plano B em vídeo).
FORMATO DA SAÍDA: roteiro slide a slide + falas-chave + tempo por bloco.
```
