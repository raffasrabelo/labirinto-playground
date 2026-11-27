# 10 · Discussão dos Resultados (texto para o TCC)

Texto da seção de discussão do capítulo **Resultados e Discussão**, comparando a plataforma e
seus resultados com outros trabalhos. Todas as referências foram conferidas nas fontes
originais em 27/11/2026 (ver "Verificação das referências" ao final).

> Os números citados vêm dos experimentos documentados em
> [06-algoritmos.md](06-algoritmos.md) (Dijkstra × Backtracking em 10 labirintos; escolha dos
> valores padrão do Q-Learning).

---

## 4.x Discussão

Objetos de aprendizagem podem ser entendidos como qualquer recurso digital que possa ser
reutilizado para apoiar a aprendizagem (WILEY, 2000). No ensino de algoritmos, porém, a
simples disponibilidade de um recurso visual não garante ganho de aprendizagem: Naps *et al.*
(2003) argumentaram que as ferramentas de visualização têm pouco valor educacional quando não
levam o aluno a uma aprendizagem ativa e propuseram uma taxonomia de engajamento, que vai de
não ver a visualização até vê-la, responder a perguntas sobre ela, alterá-la, construí-la e
apresentá-la. Sob essa ótica, o Labirinto Playground foi projetado para o nível de **alteração**:
inspirado na manipulação direta do TensorFlow Playground (SMILKOV *et al.*, 2017), o estudante
modifica o labirinto, a semente, a proporção de lama e os parâmetros de cada algoritmo e
observa imediatamente as consequências, inclusive passo a passo. Os resultados obtidos com
a própria plataforma ilustram o tipo de descoberta que esse engajamento permite. Em dez
labirintos de 21 × 21 células, o Dijkstra encontrou sempre o caminho de menor custo (média
de 97,6), enquanto o Backtracking produziu caminhos em média mais caros (143,2), embora
expandisse menos células (113,3 contra 175,6). Essa vantagem do Backtracking, contudo, não
se repetiu em todos os casos: em duas sementes ele explorou mais que o Dijkstra e ainda
assim encontrou um caminho pior, uma relação entre esforço de busca e garantia de
otimalidade que o aluno constata manipulando a ferramenta, e não apenas lendo sobre ela.

Em relação a outras ferramentas voltadas a algoritmos específicos, o VisuAlgo (HALIM *et
al.*, 2012) reúne em uma plataforma web visualizações interativas de estruturas de dados e
algoritmos, incluindo algoritmos em grafos, e Lourenço *et al.* (2022) apresentaram um objeto
de aprendizagem, implementado em Java com a biblioteca JUNG, que compara o Dijkstra, o A* e
a busca gulosa na solução do problema de caminho mínimo, com experimentos que sinalizaram
benefícios para estudantes de Ciência da Computação. O presente trabalho compartilha com
essas propostas o foco na execução visível dos algoritmos e na comparação entre eles, mas
se diferencia em três aspectos. Primeiro, reúne em um mesmo ambiente — o labirinto em grade
— algoritmos de três paradigmas distintos (busca exaustiva, otimização de caminhos e
aprendizado por reforço), o que permite comparar custo e esforço de busca sobre a mesma
instância, definida pela semente. Segundo, a lama, com custo cinco vezes maior que o das
demais células, torna visível a diferença entre o caminho com menos passos e o caminho de
menor custo, distinção central do Dijkstra. Terceiro, a plataforma executa o código em
Python diretamente no navegador, por meio de WebAssembly, sem exigir instalação, o que
reduz barreiras técnicas de acesso para o estudante ingressante.

No caso do Q-Learning, a literatura recente apresenta propostas próximas à desenvolvida,
como o Q-Learning Lab (JUENG, 2026), que exibe, em uma grade de 5 × 5 células,
os valores Q em cores, as setas da política e a atualização numérica a cada passo, e foi
avaliado quanto à corretude, por comparação com a solução obtida por iteração de valor, e
por variação dos hiperparâmetros α, γ e ε, sem estudo com estudantes. A plataforma deste
trabalho oferece recursos equivalentes — mapa de calor do valor aprendido, setas da política,
inspetor dos quatro valores Q de cada estado, seleção da grandeza exibida em todas as células
(V(s), Q(s, a) de cada ação ou número de visitas) e gráfico de recompensa por episódio —, mas
em labirintos maiores (de 11 × 11 a 31 × 31) e com custos diferenciados. De forma análoga à
validação por iteração de valor, a corretude foi verificada comparando a política aprendida
com o caminho ótimo do Dijkstra: com γ = 0,99, o agente encontrou o caminho de menor custo
nos 16 labirintos testados, enquanto, com γ = 0,95, não aprendeu o caminho em nenhum dos oito
labirintos de 21 × 21. Esse comportamento, que motivou a adoção de γ = 0,995 como valor
padrão, tornou-se ele próprio um experimento didático sobre o papel do fator de desconto.

Por outro lado, assim como o Q-Learning Lab, este trabalho ainda não mediu, com estudantes, o
efeito da plataforma sobre a aprendizagem. Os resultados apresentados mostram que a ferramenta
reproduz fielmente o comportamento dos três algoritmos e foi projetada para o nível de
alteração da taxonomia de Naps *et al.* (2003), mas os ganhos que esse engajamento pode trazer
ainda precisam ser confirmados na prática. A avaliação com estudantes ingressantes, por meio de atividades guiadas e de
questionário, constitui, portanto, o principal trabalho futuro.

---

## Referências novas (ABNT NBR 6023)

Incluir na lista de REFERÊNCIAS do TCC, em ordem alfabética junto com as demais:

HALIM, Steven; KOH, Zi Chun; LOH, Victor Bo Huai; HALIM, Felix. Learning algorithms with unified and interactive web-based visualization. **Olympiads in Informatics**, Vilnius, v. 6, p. 53-68, 2012.

JUENG, Ekkachai. **Q-Learning Lab**: teaching reinforcement learning through learner-generated trace analysis. arXiv, 2026. Preprint arXiv:2607.10802. Disponível em: https://arxiv.org/abs/2607.10802. Acesso em: 27 nov. 2026.

LOURENÇO, Wilson da Silva; ALVES, Wonder Alexandre Luz; LIMA, Stanley Jefferson de Araujo; ARAUJO, Sidnei Alves de. Objeto de aprendizagem para o ensino de algoritmos para solução do problema de caminho mínimo. **Exacta**, São Paulo, v. 22, n. 3, p. 926-939, 2022. DOI: https://doi.org/10.5585/exactaep.2022.22247.

NAPS, Thomas L. *et al.* Exploring the role of visualization and engagement in computer science education. **ACM SIGCSE Bulletin**, v. 35, n. 2, p. 131-152, 2003. DOI: https://doi.org/10.1145/960568.782998.

SMILKOV, Daniel; CARTER, Shan; SCULLEY, D.; VIÉGAS, Fernanda B.; WATTENBERG, Martin. **Direct-manipulation visualization of deep networks**. arXiv, 2017. Preprint arXiv:1708.03788. Disponível em: https://arxiv.org/abs/1708.03788. Acesso em: 27 nov. 2026.

WILEY, David A. Connecting learning objects to instructional design theory: a definition, a metaphor, and a taxonomy. *In*: WILEY, David A. (ed.). **The instructional use of learning objects**: online version. [*S. l.*: *s. n.*], 2000. Disponível em: https://mari.usc.edu/wesrac/wired/bldg-7_file/wiley.pdf. Acesso em: 27 nov. 2026.

---

## Verificação das referências

| Referência | Como foi conferida | Observação |
|---|---|---|
| Naps *et al.* (2003) | Registros da WSU, Duke e CiNii: SIGCSE Bulletin 35(2), p. 131–152, DOI 10.1145/960568.782998; taxonomia de 6 níveis | Também publicado nos ITiCSE Working Group Reports de 2002; a citação usa a versão com DOI |
| Halim *et al.* (2012) | Sumário e primeira página do volume 6 (PDF oficial): "Olympiads in Informatics, 2012, Vol. 6, 53–68", editora Vilnius University | — |
| Lourenço *et al.* (2022) | Página do artigo na Exacta: v. 22, n. 3, p. 926–939, DOI 10.5585/exactaep.2022.22247, publicado em 13/10/2022 | **O cabeçalho da edição na página diz "v. 22 n. 3 (2024)"**; a citação segue o "Como citar" e o DOI (2022). Confira com o orientador |
| Jueng (2026) | Página do arXiv 2607.10802: autor, título, grade 5 × 5, avaliações sem participantes humanos | Preprint de julho de 2026 |
| Smilkov *et al.* (2017) | Página do arXiv 1708.03788 | Preprint; versão anterior no workshop de visualização do ICML 2016 |
| Wiley (2000) | Texto integral hospedado na USC e fontes secundárias: definição "any digital resource that can be reused to support learning" | Citada de forma indireta (sem página) |

**Removidas em 27/11/2026, a pedido da equipe (P09):** Hundhausen, Douglas e Stasko (2002) e
Myers, Xie e Zhu (2020) (QUBE). O texto foi adequado sem elas, e o trecho sobre o experimento
que definiu γ = 0,995 foi mantido.

O artigo do TBC-Grafos (ICECE 2007), encontrado na busca, **não foi citado**, porque o arquivo
não pôde ser lido para conferir autores e conteúdo.
