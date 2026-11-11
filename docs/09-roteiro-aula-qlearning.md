# 09 · Roteiro de Aula: Q-Learning no Labirinto Playground

Roteiro para o uso da plataforma em sala, pensado também para que a aula seja
**documentada como caso de uso no TCC** (capítulo de Resultados).

| Campo | Preencher |
|---|---|
| Data | 12/11/2026 |
| Disciplina / turma | |
| Professor | Prof. Matheus Eloy Franco |
| Nº de estudantes | |
| Duração prevista | 30–40 min |
| Link | <https://raffasrabelo.github.io/labirinto-playground/> |

## Antes da aula (checklist)

- [ ] Abrir o link no computador do projetor **10 minutos antes**: na primeira visita o
      Python leva de 10 a 20 segundos para carregar (depois fica em cache).
- [ ] Testar no navegador da sala (Chrome, Edge ou Firefox atualizados).
- [ ] Ter o plano B aberto: as capturas em `docs/img/v0.3-qlearning-*.png`.
- [ ] Combinar com o professor quem vai registrar as observações (seção "Registro" abaixo).

## Roteiro sugerido

### 1. O problema (5 min)
Selecionar **Q-Learning**, grade **11 × 11** (treino curto, ideal para começar), e perguntar
à turma:
> "O agente não conhece o mapa. Ele só sabe onde está e recebe uma nota a cada passo.
> Como ele pode descobrir a saída?"

Explicar as recompensas mostradas no painel: −1 por passo, −5 na lama, −10 ao bater na
parede, +100 ao chegar.

### 2. Aprendendo por tentativa e erro (8 min)
1. Velocidade em **~100 passos/s** → **Executar**. A turma vê o agente (círculo laranja)
   vagando: é a fase de **exploração**.
2. Pausar e usar **Passo (N)** algumas vezes: a cada passo, uma célula da tabela Q é
   atualizada. Relacionar com a fórmula:
   `Q(s,a) ← Q(s,a) + α · [r + γ · max Q(s', ·) − Q(s,a)]`
3. Subir a velocidade. Destacar dois fenômenos:
   - **o valor se espalha a partir do objetivo:** as células roxas escuras começam perto
     da saída e "voltam" pelo labirinto;
   - **o gráfico de recompensa por episódio sobe:** o agente erra menos a cada episódio.
4. No fim, o agente percorre o caminho aprendido (verde).

### 3. Experimentos com os parâmetros (15 min)
Fazer uma pergunta, deixar a turma **prever** a resposta e só então executar.

Todos os resultados abaixo foram **verificados em 11/11/2026** com os valores padrão
(α = 0,5; γ = 0,995; ε = 0,3; decaimento 0,99; 200 episódios; +100 / −10), aberturas 10%,
lama 15% e **semente 42**. Com outra semente os números mudam, mas o comportamento é o mesmo.

| Experimento | O que mudar | Pergunta para a turma | O que acontece (verificado) |
|---|---|---|---|
| Agente "míope" | Grade **21 × 21**; γ = **0,95** | "E se o agente der menos valor ao futuro?" | **Não aprende** o caminho: a recompensa do objetivo, descontada por ~56 passos, fica pequena demais. Em **11 × 11** (caminho mais curto) ele aprende. Voltar γ = 0,995 e comparar. |
| Sem exploração | ε inicial = **0** | "Sem nunca arriscar, ele aprende?" | **Aprende**, nas duas grades. A tabela Q começa em zero e cada passo ruim vira valor negativo, então lugares não visitados parecem melhores e o agente os experimenta ("otimismo inicial"). |
| Só exploração | ε inicial = **1** e decaimento = **1** | "Agindo sempre ao acaso, ele aprende alguma coisa?" | O gráfico **fica lá embaixo** (age ao acaso o tempo todo), mas em **11 × 11 o caminho final é o ótimo**: o Q-Learning aprende a melhor política mesmo agindo aleatoriamente (*off-policy*). Em 21 × 21, 200 episódios não bastam. |
| Aprendizado lento | **11 × 11**; α = **0,05** | "E se cada experiência pesar pouco?" | Com 200 episódios **não aprende**; com **500 episódios** chega ao ótimo. |
| Lama | Lama em **40%** | "O agente percebe que a lama é cara?" | Aprende o caminho de **menor custo** (o mesmo do Dijkstra) em 11 × 11 e em 21 × 21, desviando da lama. |
| Labirinto maior | Grade **31 × 31** | "O que muda com mais estados?" | Na semente 42 aprende com 200 episódios; em outras sementes costuma precisar de **~500 episódios**. Mais estados exigem mais treino. |
| Comparação | Mesma semente, trocar para **Dijkstra** | "Qual é melhor?" | Mesmo custo final. O Dijkstra **conhece o mapa** e resolve em centenas de passos; o Q-Learning **não conhece** e precisa de dezenas de milhares de passos de tentativa e erro. |

Ao final de cada experimento, use **Restaurar valores padrão**.

> **Evite durante a aula:** grades acima de 31 × 31 no Q-Learning. O treino fica longo e o
> agente pode não convergir em 200 episódios.

### 4. Fechamento (5 min)
Perguntas para discussão:
1. O que acontece se a recompensa do objetivo for muito pequena?
   *Resposta verificada:* com **+10** no 21 × 21 ele ainda aprende, porque chegar à saída
   encerra o episódio e interrompe as penalidades de −1 por passo. Isso já é incentivo.
2. Por que o agente às vezes "anda para trás" mesmo depois de muitos episódios?
   *Resposta:* por causa da exploração (ε). Com probabilidade ε ele escolhe uma ação aleatória.
3. Onde esse tipo de aprendizado aparece fora do labirinto? (jogos, robótica, recomendação)

## Registro para o TCC (caso de uso)

Durante e logo após a aula, registrar:

- [ ] **Contexto:** disciplina, período, número de estudantes, duração.
- [ ] **Como a plataforma foi usada:** quais experimentos acima foram feitos, em que ordem.
- [ ] **Observações:** perguntas e reações dos estudantes, dúvidas que surgiram, momentos
      em que a visualização ajudou ou atrapalhou.
- [ ] **Problemas técnicos:** tempo de carregamento, travamentos, navegador usado.
- [ ] **Depoimento do professor** (2–3 frases) sobre o uso em aula.
- [ ] **Fotos** da aula **apenas com autorização** e sem rostos identificáveis.
- [ ] (Opcional) **Questionário anônimo** de 3–5 perguntas em escala de 1 a 5, por exemplo:
      "A visualização me ajudou a entender o papel do γ"; "Eu conseguiria explicar o que é a
      tabela Q para um colega".

> **Ética:** pesquisas com estudantes podem exigir aprovação do Comitê de Ética (risco R4 do
> [cronograma](04-cronograma.md#riscos-e-plano-de-corte)). Um questionário **anônimo de
> opinião**, sem dados pessoais, costuma ser dispensado, mas **confirme com o orientador**
> antes de aplicar.

### Como isso entra no texto
Sugestão de estrutura para a seção do capítulo de Resultados:
1. **Contexto da aplicação:** turma, data, objetivo da aula.
2. **Procedimento:** o roteiro acima, resumido.
3. **Observações:** o que foi registrado, com as capturas de tela como figuras.
4. **Discussão:** relação com a questão de pesquisa (redução da dificuldade de abstração).
5. **Limitações:** uma única turma e uma única aula, sem grupo de controle.

Figuras disponíveis (legendas no padrão ABNT em [08-legendas-das-figuras.md](08-legendas-das-figuras.md)):
`v0.3-qlearning-treinando.png`, `v0.3-qlearning-concluido.png`, `v0.3-qlearning-gama-095.png`.
