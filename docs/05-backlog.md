# 05 · Product Backlog

Prioridade **MoSCoW**: Must (obrigatório) · Should (importante) · Could (desejável) · Won't (fora do escopo agora).
Status: ✅ pronto · 🔄 em andamento · ⏳ a fazer · ✂️ cortado.

## Épico E1 · Fundação e motor do labirinto
| ID | História de usuário | Prior. | Sprint | Status |
|---|---|---|---|---|
| US-01 | Como aluno, quero ver um labirinto gerado automaticamente para começar sem configurar nada | Must | S0 | ✅ |
| US-02 | Como aluno, quero alterar tamanho, aberturas, lama e semente e ver o labirinto mudar na hora | Must | S0 | ✅ |
| US-03 | Como aluno, quero desenhar paredes e lama e mover início e objetivo com o mouse para testar hipóteses | Must | S0 | ✅ |
| US-04 | Como aluno, quero executar, pausar, avançar um passo e mudar a velocidade para acompanhar no meu ritmo | Must | S0 | ✅ |
| US-05 | Como aluno, quero métricas e legenda para interpretar o que vejo | Must | S0 | ✅ |

## Épico E2 · Plataforma web
| ID | História de usuário | Prior. | Sprint | Status |
|---|---|---|---|---|
| US-06 | Como aluno, quero abrir a plataforma por um link, sem instalar nada | Must | S0/S1 | 🔄 roda no navegador (local); falta o link público |
| US-07 | Como equipe, queremos publicar automaticamente a cada sprint para os stakeholders testarem | Should | S1 | ⏳ |
| US-08 | Como equipe, queremos medir o FPS no navegador e ajustar os limites de tamanho | Must | S0 | ✅ 61×61 cabe em 60 fps (P01) |

## Épico E3 · Dijkstra
| ID | História de usuário | Prior. | Sprint | Status |
|---|---|---|---|---|
| US-09 | Como aluno, quero ver a distância acumulada em cada célula | Should | S0 | ✅ |
| US-10 | Como aluno, quero ver o pseudocódigo com a linha atual destacada | Should | S1 | ⏳ |
| US-11 | Como aluno, quero ver o conteúdo da fila de prioridade (próximas células e distâncias) | Should | S1 | ⏳ |

## Épico E4 · Backtracking
| ID | História de usuário | Prior. | Sprint | Status |
|---|---|---|---|---|
| US-12 | Como aluno, quero ver a pilha de chamadas recursivas crescendo e encolhendo | Must | S2 | ⏳ |
| US-13 | Como aluno, quero escolher a ordem de exploração dos vizinhos e ver o resultado mudar | Could | S2 | ⏳ |
| US-14 | Como aluno, quero um modo exaustivo (todas as soluções) em grades pequenas para entender a explosão combinatória | Could | S2 | ⏳ |
| US-15 | Como aluno, quero ver o pseudocódigo recursivo com a linha atual destacada | Should | S2 | ⏳ |

## Épico E5 · Q-Learning
| ID | História de usuário | Prior. | Sprint | Status |
|---|---|---|---|---|
| US-16 | Como aluno, quero treinar um agente ajustando α, γ, ε e nº de episódios | Must | S3 | ⏳ |
| US-17 | Como aluno, quero configurar as recompensas (objetivo, passo, lama, parede) | Should | S3 | ⏳ |
| US-18 | Como aluno, quero ver um mapa de calor do valor aprendido e setas da política | Must | S3 | ⏳ |
| US-19 | Como aluno, quero ver a curva de recompensa por episódio | Should | S3 | ⏳ |
| US-20 | Como aluno, quero assistir ao agente treinado percorrer o labirinto | Must | S3 | ⏳ |

## Épico E6 · Validação e acabamento
| ID | História de usuário | Prior. | Sprint | Status |
|---|---|---|---|---|
| US-21 | Como aluno de primeiro acesso, quero um tutorial curto | Could | S4 | ⏳ |
| US-22 | Como aluno, quero comparar dois algoritmos no mesmo labirinto, lado a lado | Could | S4 | ⏳ |
| US-23 | Como pesquisadores, queremos aplicar um roteiro de uso + questionário com alunos | Should | S4 | ⏳ |
| US-24 | Como equipe, queremos revisar a acessibilidade de cores (daltonismo/contraste) | Should | S4 | ⏳ |
| US-25 | Como equipe, queremos a v1.0 congelada, vídeo de demonstração e slides | Must | S5 | ⏳ |

## Itens técnicos (dívida/infra)
| ID | Item | Sprint | Status |
|---|---|---|---|
| T-01 | Arquitetura de geradores de eventos + testes automatizados | S0 | ✅ |
| T-02 | Repositório GitHub + tags por sprint | S1 | ⏳ |
| T-03 | Redesenhar só as células alteradas (se o FPS web for baixo) | S1 | ⏳ |
