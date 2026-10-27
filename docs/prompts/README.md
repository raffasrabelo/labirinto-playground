# Registro de Prompts

Esta pasta documenta o uso de IA generativa no desenvolvimento, para que ele possa ser
**citado no TCC** (Metodologia e Apêndice) e auditado pelos stakeholders.

## Como funciona

1. Antes de pedir algo à IA, copie o prompt correspondente do [catálogo](catalogo.md)
   (ou escreva um novo usando o [modelo](_modelo-prompt.md)).
2. Depois da resposta, crie um arquivo `PXX-titulo-curto.md` (ex.: `P01-build-web.md`) com o
   registro preenchido: o que foi pedido, o que foi gerado, **o que a equipe mudou** e onde o
   resultado foi parar (arquivos e commit).
3. Atualize a tabela de índice abaixo.

> A conversa de **planejamento inicial do projeto não entra neste registro** (decisão da equipe).
> O registro começa no P01.

## Estrutura padrão de um prompt

Todo prompt segue seis blocos. Assim ele fica reproduzível e fácil de citar:

| Bloco | Pergunta que responde |
|---|---|
| **Papel** | Que tipo de especialista a IA deve ser? |
| **Contexto** | Em que ponto o projeto está? Que arquivos importam? |
| **Tarefa** | O que exatamente deve ser feito nesta interação? |
| **Restrições** | O que não pode mudar? Que tecnologias usar ou evitar? |
| **Critérios de aceite** | Como saberemos que ficou pronto? |
| **Formato da saída** | Código, documento, lista, diagrama? |

## Índice de prompts executados

| ID | Data | Sprint | Item do backlog | Título | Autor |
|---|---|---|---|---|---|
| [P01](P01-build-web.md) | 27/10/2026 | S0 | US-06, US-08 | Build web com pygbag | Rafael |

## Sugestão de texto para o TCC (Metodologia)

> "Durante o desenvolvimento, utilizou-se um assistente de IA generativa (Claude Code,
> Anthropic) como apoio à programação e à documentação. As interações foram estruturadas
> em prompts padronizados (papel, contexto, tarefa, restrições, critérios de aceite e formato
> de saída) e registradas integralmente no Apêndice X, junto com as alterações feitas pelos
> autores. Todo código gerado foi revisado, testado por meio de testes automatizados e
> validado nas Sprint Reviews, sendo a responsabilidade pelo conteúdo final dos autores."

*(Confirmar com o orientador se a instituição tem regras específicas sobre a declaração de uso de IA.)*
