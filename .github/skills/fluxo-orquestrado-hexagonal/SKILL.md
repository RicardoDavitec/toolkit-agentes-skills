---
name: fluxo-orquestrado-hexagonal
description: 'Orquestra fluxo completo de desenvolvimento hexagonal. Use para quebrar trabalho em etapas e delegar para agentes especializados com foco em seguranca e entrega.'
argument-hint: 'Objetivo, escopo, restricoes e criterio de pronto'
user-invocable: true
---

# Fluxo Orquestrado Hexagonal

## Quando usar
- Tarefas grandes com multiplas etapas.
- Mudancas que misturam arquitetura, implementacao e operacao.
- Situacoes com risco alto de regressao.

## Etapas
1. Entendimento e corte de escopo.
2. Revisao arquitetural de limites (guardrails-hexagonal).
3. Revisao de contratos (checar-contratos-portas).
4. Revisao de caso de uso (revisar-casos-de-uso).
5. Implementacao controlada e validacao.
6. Gate de release (gate-release-hexagonal).
7. Documentacao final (documentar-sessao).
8. Fechamento (encerrar-sessao).

## Delegacao sugerida por etapa
- Etapas 2 e 3: Revisor Arquitetura Hexagonal.
- Etapa 5: Operador Entrega Controlada.
- Falhas em integracao externa: Analista Incidentes Integracao.

## Script de apoio
- [Gerar checklist de execucao](./scripts/gerar_checklist_fluxo.py)

## Criterio de Conclusao
- Entrega com evidencias de validacao, risco residual descrito e proximo passo definido.
