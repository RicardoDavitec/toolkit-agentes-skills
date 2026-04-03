---
name: gate-release-hexagonal
description: 'Aplica gate de release para projeto hexagonal. Use antes de deploy/publicacao para validar testes, riscos, contratos, rollback e documentacao minima da entrega.'
argument-hint: 'Escopo da release e ambiente alvo'
user-invocable: true
---

# Gate Release Hexagonal

## Quando usar
- Antes de deploy em ambiente compartilhado.
- Antes de publicacao de marco funcional.

## Procedimento
1. Validar testes relevantes.
2. Validar contratos de portas e adaptadores.
3. Revisar risco operacional e rollback.
4. Confirmar atualizacao de documentacao essencial.
5. Emitir status: aprovado, aprovado com ressalvas, reprovado.

## Criterio de Conclusao
- Decisao de release registrada com evidencias tecnicas.
