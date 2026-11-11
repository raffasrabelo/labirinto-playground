# 03 · Processo de Trabalho (Scrum adaptado)

O TCC (cap. 3.1) já define o uso de **Scrum**. Este documento descreve como ele
é aplicado a uma equipe de duas pessoas com dois stakeholders acadêmicos.

| Diagrama | Tipo | Pergunta que responde |
|---|---|---|
| [Visão geral do Scrum](#visão-geral-do-scrum-no-projeto) | fluxograma em blocos | Quais são os papéis, eventos e artefatos? |
| [Ciclo da sprint](#ciclo-da-sprint-1-semana-quinta--quarta) | fluxograma | Em que ordem as coisas acontecem? |
| [Semana típica](#semana-típica-de-sprint) | Gantt | Em que dia acontece cada atividade? |
| [Quem faz o quê](#quem-faz-o-quê) | sequência (colunas = raias) | Qual papel executa cada passo? |
| [Ciclo de vida de um item](#ciclo-de-vida-de-um-item-do-backlog) | diagrama de estados | Por quais estados uma tarefa passa? |
| [Fluxo do feedback](#fluxo-do-feedback) | fluxograma de decisão | O que acontece com cada comentário dos stakeholders? |
| [Fluxo de código](#fluxo-de-código-git) | gitGraph | Como o código chega à `main` e vira versão? |
| [Uso de IA](#uso-de-ia-generativa-no-projeto) | diagrama de sequência | Como um prompt vira código e registro? |

## Papéis

| Papel Scrum | Quem | Responsabilidade |
|---|---|---|
| Stakeholder principal / "cliente" | Orientador | Valida o incremento e prioriza junto com a equipe |
| Stakeholder | Professora da disciplina de TCC | Acompanha prazos, normas e escrita |
| Product Owner | *(definir: um dos alunos)* | Mantém o backlog e traduz o feedback em itens |
| Scrum Master | *(definir: o outro aluno, ou revezamento)* | Garante as cerimônias e os registros |
| Time de desenvolvimento | Arielce e Rafael | Código, testes, documentação e escrita |

> Como a equipe é pequena, os papéis de PO e SM são acumulados. Escrever isso no TCC
> como adaptação consciente do Scrum é melhor do que fingir uma equipe completa.

## Visão geral do Scrum no projeto

Os três pilares do Scrum (papéis, eventos e artefatos) e onde cada artefato fica no repositório.

```mermaid
flowchart TB
    subgraph PAPEIS["Papéis"]
        direction LR
        ST["Stakeholders<br/>orientador + professora"]
        PO["Product Owner<br/>(aluno)"]
        SM["Scrum Master<br/>(aluno)"]
        DT["Time de desenvolvimento<br/>Arielce + Rafael"]
    end
    subgraph EVENTOS["Eventos (sprint de 1 semana)"]
        direction LR
        E1(["Planning<br/>quinta"]) --> E2(["Daily assíncrona<br/>dias úteis"]) --> E3(["Sprint Review<br/>quarta"]) --> E4(["Retrospectiva<br/>quarta"])
    end
    subgraph ARTEFATOS["Artefatos"]
        direction LR
        A1[("Product Backlog<br/>docs/05-backlog.md")]
        A2[("Sprint Backlog<br/>docs/sprints/sprint-N.md")]
        A3[("Incremento<br/>link público + tag sprint-N")]
        A4[("Registro de prompts<br/>docs/prompts/")]
    end
    PO -- "prioriza (MoSCoW)" --> A1
    A1 -- "Planning" --> A2
    DT -- "constrói" --> A3
    DT -- "registra" --> A4
    ST -- "avaliam na Review" --> A3
    SM -. "facilita" .-> EVENTOS
    E3 -- "feedback" --> A1
```

## Ciclo da sprint (1 semana: quinta → quarta)

Desenhado em **retrato** para caber na largura da página do TCC (proporção altura/largura de
cerca de 1,4, perto da área útil de uma folha A4). Como ler:
- a **espinha central** são os eventos da sprint, de cima para baixo;
- ao lado de cada evento fica o **artefato** que ele gera (linha pontilhada);
- tudo entre a *Sprint Planning* e a *Retrospectiva* acontece dentro da sprint de 1 semana;
- a seta da direita fecha o ciclo e volta ao *Product Backlog* para a próxima sprint.

Retângulos azuis são **eventos**; cilindros cinza são **artefatos**.

```mermaid
flowchart TB
    PB[("Product Backlog<br/>05-backlog.md")] --> PL["Sprint Planning<br/>quinta · 30 min"]
    SB[("Sprint Backlog<br/>sprint-N.md")]
    DEV["Desenvolvimento<br/>código, testes e<br/>escrita do TCC"]
    DAILY{{"Daily assíncrona<br/>todo dia útil"}}
    DOD{"Atende à<br/>Definition<br/>of Done?"}
    INC[("Incremento<br/>link público + tag")]
    REV["Sprint Review<br/>quarta · com stakeholders"]
    FB[("Registro de<br/>feedback")]
    RET["Retrospectiva<br/>quarta · 15 min"]

    PL --> DEV
    PL -. "gera" .-> SB
    DAILY <-.-> DEV
    DEV --> DOD
    DOD -- "não" --> DEV
    DOD -- "sim" --> REV
    DOD -. "gera" .-> INC
    REV --> RET
    REV -. "gera" .-> FB
    RET -- "próxima sprint" --> PB

    classDef evento fill:#eaf1fe,stroke:#2f6fed,color:#1d2939
    classDef artefato fill:#f2f4f7,stroke:#667085,color:#1d2939
    class PL,DEV,REV,RET evento
    class PB,SB,INC,FB artefato
```

### Cerimônias

| Cerimônia | Quando | Duração | Saída registrada |
|---|---|---|---|
| **Planning** | Quinta | 30 min | Sprint Goal + itens escolhidos em `sprint-N.md` |
| **Daily** (assíncrona) | Todo dia útil | 2 min | Mensagem no grupo: *fiz / vou fazer / impedimento* |
| **Sprint Review** | Quarta | 15–20 min | Demo + feedback na tabela da sprint |
| **Retrospectiva** | Quarta, após a review | 15 min | *manter / melhorar / experimentar* |

### Roteiro padrão da Sprint Review (≈15 min)
1. Sprint Goal e o que foi concluído (1 min).
2. **Demonstração ao vivo** do incremento (5–7 min).
3. O que não foi concluído e por quê (1 min).
4. Plano da próxima sprint (2 min).
5. **Perguntas direcionadas** aos stakeholders (5 min). Sempre levar 3 a 5 perguntas prontas: o feedback fica muito melhor do que só perguntar "o que acharam?".

## Semana típica de sprint

Exemplo com as datas da Sprint 1. Fins de semana e o feriado de Finados (02/11) aparecem como
intervalos sem trabalho.

```mermaid
gantt
    title Semana típica de sprint (exemplo: Sprint 1)
    dateFormat YYYY-MM-DD
    axisFormat %d/%m
    excludes weekends, 2026-11-02
    section Cerimônias
    Planning (30 min)              :milestone, p, 2026-10-29, 0d
    Daily assíncrona               :d, 2026-10-29, 5d
    Sprint Review + Retrospectiva  :milestone, r, 2026-11-04, 0d
    section Desenvolvimento
    Implementar itens da sprint    :dev, 2026-10-29, 3d
    Testes + correções             :t, after dev, 1d
    Congelar incremento e publicar :pub, after t, 1d
    section Escrita do TCC
    Rascunho da seção da sprint    :w, 2026-10-30, 3d
    Revisão do texto               :wr, after w, 1d
    section Registro
    Prompts PXX e sprint-N.md      :reg, 2026-10-29, 5d
```

## Quem faz o quê

Cada coluna funciona como uma **raia** (um participante). As setas são as passagens de bastão
e as notas são o que cada um faz na sua vez.

```mermaid
sequenceDiagram
    participant ST as Stakeholders
    participant PO as Product Owner
    participant T as Time
    participant IA as Assistente de IA
    participant GH as GitHub
    ST->>PO: feedback da Review anterior
    Note over PO: transforma em itens do backlog<br/>e prioriza (MoSCoW)
    PO->>T: propõe o Sprint Goal (Planning)
    Note over T: seleciona os itens<br/>e cria sprint-N.md
    loop cada item da sprint
        T->>IA: prompt do catálogo + contexto
        IA-->>T: código, testes e documentação
        Note over T: revisa, testa e registra PXX
        T->>GH: git push
        Note over GH: pytest → build → Pages
        GH-->>T: link público atualizado
    end
    Note over T: escreve a seção do TCC
    T->>ST: demonstra na Sprint Review
    ST-->>PO: novo feedback
```

## Ciclo de vida de um item do backlog

```mermaid
stateDiagram-v2
    state "Ideia" as Ideia
    state "No backlog" as Backlog
    state "Selecionado na sprint" as Sel
    state "Em andamento" as Dev
    state "Em revisão (DoD)" as Rev
    state "Pronto" as Pronto
    state "Demonstrado" as Demo
    state "Cortado" as Cortado

    [*] --> Ideia: feedback, requisito ou bug
    Ideia --> Backlog: PO escreve a história + MoSCoW
    Backlog --> Sel: Planning
    Sel --> Backlog: não coube na sprint
    Sel --> Dev: alguém assume
    Dev --> Rev: código + testes + registro
    Rev --> Dev: falhou em algum item da DoD
    Rev --> Pronto: DoD atendida
    Pronto --> Demo: Sprint Review
    Demo --> [*]
    Backlog --> Cortado: linha de corte do cronograma
    Cortado --> [*]
```

## Fluxo do feedback

```mermaid
flowchart LR
    A[Stakeholder comenta] --> B[Registrar na tabela de<br/>feedback da sprint]
    B --> C{Tipo}
    C -- "bug / ajuste pequeno" --> D[Item na próxima sprint]
    C -- "nova funcionalidade" --> E[Product Backlog<br/>com prioridade MoSCoW]
    C -- "mudança de escopo/prazo" --> F[Atualizar cronograma<br/>+ histórico de alterações]
    C -- "texto do TCC" --> G[Pendência de escrita]
    D & E & F & G --> H[Confirmar na próxima Review<br/>que o feedback foi atendido]
```

## Definition of Done (DoD)

Um item só está **pronto** quando:
- [ ] o código está no repositório (branch `main`) e os testes (`pytest`) passam;
- [ ] funciona na versão web (a partir da S1);
- [ ] foi demonstrado ou é demonstrável na Review;
- [ ] os prompts de IA usados estão registrados em `docs/prompts/`;
- [ ] a documentação afetada (requisitos, arquitetura, backlog) foi atualizada;
- [ ] **a parte correspondente do texto do TCC foi escrita** (mesmo que em rascunho).

## Fluxo de código (Git)

- `main` sempre funcionando; trabalho em branches `feat/US-xx-descricao`.
- Commits no padrão *Conventional Commits*: `feat:`, `fix:`, `docs:`, `test:`, `refactor:`.
- Ao fim de cada sprint: tag `sprint-N` (ex.: `sprint-0`). Cada tag é um incremento citável no TCC.
- Todo push na `main` dispara testes e publicação (ver [02-arquitetura.md](02-arquitetura.md#fluxo-de-build-e-publicação)).
- O repositório está hoje na pasta do OneDrive. Se a sincronização causar problemas na pasta
  `.git`, clone o repositório em uma pasta fora do OneDrive e trabalhe a partir dela.

Fluxo **previsto** a partir da Sprint 1 (na Sprint 0 os commits foram direto na `main`):

```mermaid
gitGraph
    commit id: "v0.1 protótipo"
    commit id: "docs: P02"
    commit id: "feat: interface HTML (v0.2)" tag: "sprint-0"
    branch feat/US-10-pseudocodigo
    checkout feat/US-10-pseudocodigo
    commit id: "painel de pseudocódigo"
    commit id: "test: linha ativa"
    checkout main
    merge feat/US-10-pseudocodigo
    branch fix/T-04-actions
    checkout fix/T-04-actions
    commit id: "atualiza actions"
    checkout main
    merge fix/T-04-actions
    commit id: "docs: P04, sprint-01" tag: "sprint-1"
```

## Uso de IA generativa no projeto

O desenvolvimento usa um assistente de IA (Claude Code) como **par de programação**. Para
transparência acadêmica:
- todo prompt relevante é registrado em `docs/prompts/` (o que foi pedido, o que foi
  gerado, o que a equipe revisou ou alterou);
- toda saída é revisada, testada e assumida pela equipe;
- o TCC deve declarar esse uso na Metodologia (sugestão de texto em `docs/prompts/README.md`).
  **Confirme com o orientador as regras da instituição.**

```mermaid
sequenceDiagram
    actor E as Equipe
    participant C as Catálogo (Cxx)
    participant IA as Assistente de IA
    participant R as Repositório
    participant P as Registro (Pxx)
    E->>C: escolhe o prompt do item da sprint
    E->>E: ajusta o CONTEXTO com o feedback da Review
    E->>IA: envia o prompt
    IA->>R: lê código e documentação
    IA-->>E: propõe alterações, testes e evidências
    E->>E: revisa, executa pytest e testa no navegador
    alt aprovado (com ou sem ajustes)
        E->>R: commit + push (dispara publicação)
        E->>P: registra pedido, resultado e revisão da equipe
    else rejeitado
        E->>P: registra o que foi rejeitado e por quê
    end
```
